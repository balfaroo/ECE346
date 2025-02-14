from typing import Tuple, Optional, Dict, Union
from jaxlib.xla_extension import ArrayImpl
import time
import os
import numpy as np
import jax
from .dynamics import Bicycle5D
from .cost import Cost, CollisionChecker, Obstacle
from .ref_path import RefPath
from .config import Config
import time

status_lookup = ['Iteration Limit Exceed',
                'Converged',
                'Failed Line Search']

class ILQR():
	def __init__(self, config_file = None) -> None:

		self.config = Config()  # Load default config.
		if config_file is not None:
			self.config.load_config(config_file)  # Load config from file.
		
		self.load_parameters()
		print('ILQR setting:', self.config)

		# Set up Jax parameters
		jax.config.update('jax_platform_name', self.config.platform)
		print('Jax using Platform: ', jax.lib.xla_bridge.get_backend().platform)

		# If you want to use GPU, lower the memory fraction from 90% to avoid OOM.
		os.environ['XLA_PYTHON_CLIENT_MEM_FRACTION'] = '20'

		self.dyn = Bicycle5D(self.config)
		self.cost = Cost(self.config)
		self.ref_path = None

		# collision checker
		# Note: This will not be used until lab2.
		self.collision_checker = CollisionChecker(self.config)
		self.obstacle_list = []
		
		# Do a dummy run to warm up the jitted functions.
		self.warm_up()

	def load_parameters(self):
		'''
		This function defines ILQR parameters from <self.config>.
		'''
		# ILQR parameters
		self.dim_x = self.config.num_dim_x
		self.dim_u = self.config.num_dim_u
		self.T = int(self.config.T)
		self.dt = float(self.config.dt)
		self.max_iter = int(self.config.max_iter)
		self.tol = float(self.config.tol)  # ILQR update tolerance.

		# line search parameters.
		self.alphas = self.config.line_search_base**(
						np.arange(self.config.line_search_a,
                        self.config.line_search_b,
                        self.config.line_search_c)
                    )

		print('Line Search Alphas: ', self.alphas)

		# regularization parameters
		self.reg_min = float(self.config.reg_min)
		self.reg_max = float(self.config.reg_max)
		self.reg_init = float(self.config.reg_init)
		self.reg_scale_up = float(self.config.reg_scale_up)
		self.reg_scale_down = float(self.config.reg_scale_down)
		self.max_attempt = self.config.max_attempt
		
	def warm_up(self):
		'''
		Warm up the jitted functions.
		'''
		# Build a fake path as a 1 meter radius circle.
		theta = np.linspace(0, 2 * np.pi, 100)
		centerline = np.zeros([2, 100])
		centerline[0,:] = 1 * np.cos(theta)
		centerline[1,:] = 1 * np.sin(theta)

		self.ref_path = RefPath(centerline, 0.5, 0.5, 1, True)

		# add obstacle
		obs = np.array([[0, 0, 0.5, 0.5], [1, 1.5, 1, 1.5]]).T
		obs_list = [[obs for _ in range(self.T)]]
		self.update_obstacles(obs_list)

		x_init = np.array([0.0, -1.0, 1, 0, 0])
		print('Start warm up ILQR...')
		self.plan(x_init)
		print('ILQR warm up finished.')
		
		self.ref_path = None
		self.obstacle_list = []

	def update_ref_path(self, ref_path: RefPath):
		'''
		Update the reference path.
		Args:
			ref_path: RefPath: reference path.
		'''
		self.ref_path = ref_path

	def update_obstacles(self, vertices_list: list):
		'''
		Update the obstacle list for a list of vertices.
		Args:
			vertices_list: list of np.ndarray: list of vertices for each obstacle.
		'''
		# Note: This will not be used until lab2.
		self.obstacle_list = []
		for vertices in vertices_list:
			self.obstacle_list.append(Obstacle(vertices))

	def get_references(self, trajectory: Union[np.ndarray, ArrayImpl]):
		'''
		Given the trajectory, get the path reference and obstacle information.
		Args:
			trajectory: [num_dim_x, T] trajectory.
		Returns:
			path_refs: [num_dim_x, T] np.ndarray: references.
			obs_refs: [num_dim_x, T] np.ndarray: obstacle references.
		'''
		trajectory = np.asarray(trajectory)
		path_refs = self.ref_path.get_reference(trajectory[:2, :])
		obs_refs = self.collision_checker.check_collisions(trajectory, self.obstacle_list)
		return path_refs, obs_refs



	def forward_pass(self, nom_traj, nom_control, J_bar, K_arr, k_arr, path_refs, obs_refs, init_alpha = 0.5, rho=0.0001, epsilon = 0.9):
		alpha = 0.1

		x_arr = np.empty_like(nom_traj)
		u_arr = np.empty_like(nom_control)

		x_arr[:, 0] = nom_traj[:,0]

		while alpha > rho:
			for t in range(0, self.T-1):
				u_arr[:, t] = nom_control[:, t] + K_arr[:, :, t] @ (x_arr[:,t] - nom_traj[:, t]) + alpha*k_arr[:, t]
				x_arr[:, t + 1], u_arr[:, t] = self.dyn.integrate_forward_np(x_arr[:, t], u_arr[:, t])

			J = self.cost.get_traj_cost(x_arr, u_arr, path_refs, obs_refs)

			if J < J_bar:
				break
			else:
				alpha = epsilon*alpha

		return x_arr, u_arr, J


	def backward_pass(self, nom_traj, nom_control, lam, path_refs, obs_refs, a = 1.1, b = 0.9):
		'''
		print('called backward pass')
		print(nom_traj)
		print()
		print(nom_control)
		print()
		print(lam)
		print()
		print(path_refs)
		print()
		print(obs_refs)
		'''
		q, r, Q, R, H = self.cost.get_derivatives_np(nom_traj, nom_control, path_refs, obs_refs)
		A, B = self.dyn.get_jacobian_np(nom_traj, nom_control)
		
		p, P = q[:,self.T-1], Q[:,:,self.T-1]
		t = self.T - 2

		K_arr = np.zeros((nom_control.shape[0], nom_traj.shape[0], self.T))
		k_arr = np.zeros((nom_control.shape[0], self.T))
	
		#print(np.shape(K_arr))

		while t >= 0:
			'''
			try:
				#q, r, Q, R, H = self.cost.get_derivatives_np(nom_traj[:, :t], nom_control[:, :t], path_refs[:, :t], obs_refs[:, :, :t])
			except:
				print(np.shape(nom_traj[:, :t]))
				print()
				print(np.shape(nom_control[:, :t]))
				print()
				print(np.shape(path_refs[:, :t]))
				print()
				print(np.shape(obs_refs[:, :, :t]))
				raise Exception("fools")
			'''

			Q_xt = q[:,t] + A[:,:,t].T@p
			Q_ut = r[:,t] + B[:,:,t].T@p
			Q_xxt = Q[:,:,t] + A[:,:,t].T@P@A[:,:,t]
			Q_uut = R[:,:,t] + B[:,:,t].T@P@B[:,:,t]
			Q_uxt = H[:,:,t] + B[:,:,t].T@P@A[:,:,t]

			Q_reg_uut = R[:,:,t] + B[:,:,t].T@(P + lam*np.identity(P.shape[0]))@B[:,:,t]
			Q_reg_uxt = H[:,:,t] + B[:,:,t].T@(P + lam*np.identity(P.shape[0]))@A[:,:,t]
			
			if  not np.all(np.linalg.eigvals(Q_reg_uut) > 0):
                
				if lam < self.max_attempt:
					lam = lam * self.reg_scale_up
					t = self.T - 2
					p = q[:, self.T-1]
					P = Q[:,:,self.T-1]
					continue

			K = -np.linalg.inv(Q_reg_uut)@Q_reg_uxt
			k = -np.linalg.inv(Q_reg_uut)@Q_ut

			K_arr[:, :, t] = K
			k_arr[:, t] = k

			p = Q_xt + K.T@Q_ut + K.T@Q_uut@k + Q_uxt.T@k
			P = Q_xxt + K.T@Q_uut@K + K.T@Q_uxt + Q_uxt.T@K
			
			t = t - 1

		return K_arr, k_arr, max(self.reg_min, lam*self.reg_scale_down)



	def plan(self, init_state: np.ndarray,
                controls: Optional[np.ndarray] = None) -> Dict:
		'''
        Main ILQR loop.
        Args:
            init_state: [num_dim_x] np.ndarray: initial state.
            control: [num_dim_u, T] np.ndarray: initial control.
        Returns:
            A dictionary with the following keys:
                status: int: -1 for failure, 0 for success. You can add more status if you want.
                t_process: float: time spent on planning.
                trajectory: [num_dim_x, T] np.ndarray: ILQR planned trajectory.
                controls: [num_dim_u, T] np.ndarray: ILQR planned controls sequence.
                K_closed_loop: [num_dim_u, num_dim_x, T] np.ndarray: closed loop gain.
                k_closed_loop: [num_dim_u, T] np.ndarray: closed loop bias.
        '''

        # We first check if the planner is ready
		if self.ref_path is None:
			print('No reference path is provided.')
			return dict(status=-1)

        # if no initial control sequence is provided, we assume it is all zeros.
		if controls is None:
			controls =np.zeros((self.dim_u, self.T))
		else:
			assert controls.shape[1] == self.T

        # Start timing
		t_start = time.time()

        # Rolls out the nominal trajectory and gets the initial cost.
		trajectory, controls = self.dyn.rollout_nominal_np(init_state, controls)

        # Get path and obstacle references based on your current nominal trajectory.
        # Note: you will NEED TO call this function and get new references at each iteration.
		path_refs, obs_refs = self.get_references(trajectory)

        # Get the initial cost of the trajectory.
		J = self.cost.get_traj_cost(trajectory, controls, path_refs, obs_refs)

        ##########################################################################
        # TODO 1: Implement the ILQR algorithm. Feel free to add any helper functions.
        # You will find following implemented functions useful:

        # ******** Functions to compute the Jacobians of the dynamics  ************
        # A, B = self.dyn.get_jacobian_np(trajectory, controls)

        # Returns the linearized 'A' and 'B' matrix of the ego vehicle around
        # nominal trajectory and controls.

        # Args:
        #   trajectory: np.ndarray, (dim_x, T) trajectory along the nominal trajectory.
        #   controls: np.ndarray, (dim_u, T) controls along the trajectory.

        # Returns:
        #   A: np.ndarray, (dim_x, T) the Jacobian of the dynamics w.r.t. the state.
        #   B: np.ndarray, (dim_u, T) the Jacobian of the dynamics w.r.t. the control.
        
        # ******** Functions to roll the dynamics for one step  ************
        # state_next, control_clip = self.dyn.integrate_forward_np(state, control)
        
        # Finds the next state of the vehicle given the current state and
        # control input.

        # Args:
        #   state: np.ndarray, (dim_x).
        #   control: np.ndarray, (dim_u).

        # Returns:
        #   state_next: np.ndarray, (dim_x) next state.
        #   control_clip: np.ndarray, (dim_u) clipped control.
        
        # *** Functions to get total cost of a trajectory and control sequence  ***
        # J = self.cost.get_traj_cost(trajectory, controls, path_refs, obs_refs)
        # Given the trajectory, control seq, and references, return the sum of the cost.
        # Input:
        #   trajectory: (dim_x, T) array of state trajectory
        #   controls:   (dim_u, T) array of control sequence
        #   path_refs:  (dim_ref, T) array of references (e.g. reference path, reference velocity, etc.)
        #   obs_refs: *Optional* (num_obstacle, (2, T)) List of obstacles. Default to None
        # return:
        #   cost: float, sum of the running cost over the trajectory

        # ******** Functions to get jacobian and hessian of the cost ************
        # q, r, Q, R, H = self.cost.get_derivatives_np(trajectory, controls, path_refs, obs_refs)
        
        # Given the trajectory, control seq, and references, return Jacobians and Hessians of cost function
        # Input:
        #   trajectory: (dim_x, T) array of state trajectory
        #   controls:   (dim_u, T) array of control sequence
        #   path_refs:  (dim_ref, T) array of references (e.g. reference path, reference velocity, etc.)
        #   obs_refs: *Optional* (num_obstacle, (2, T)) List of obstacles. Default to None
        # return:
        #   q: np.ndarray, (dim_x, T) jacobian of cost function w.r.t. states
        #   r: np.ndarray, (dim_u, T) jacobian of cost function w.r.t. controls
        #   Q: np.ndarray, (dim_x, dim_u, T) hessian of cost function w.r.t. states
        #   R: np.ndarray, (dim_u, dim_u, T) hessian of cost function w.r.t. controls
        #   H: np.ndarray, (dim_x, dim_u, T) hessian of cost function w.r.t. states and controls
        
        ########################### #END of TODO 1 #####################################

		lam = self.reg_init      #lambda_0
		J_new = np.infty
		status = 0
		first = True
	

		'''
		while (abs(J_new - J) > 1e-5):
			if not first:
				J = J_new
			#J = J_new
			try:
				K_arr, k_arr, lam = self.backward_pass(trajectory, controls, lam, path_refs, obs_refs)
			except:
				#print('failed on iteration %d' % counter)
				raise Exception('found the nans')
			trajectory, controls, J_new = self.forward_pass(trajectory, controls, J, K_arr, k_arr, path_refs, obs_refs)
			if J_new > J:
				status = -1
				break

			if first:
				first = False
		'''
		converged = False
		#print('ilqr started')

		for _ in range(self.max_iter):
			K_arr, k_arr, lam = self.backward_pass(trajectory, controls, lam, path_refs, obs_refs)
			changed = False
			for alpha in self.alphas:
				x_arr = np.empty_like(trajectory)
				u_arr = np.empty_like(controls)
				x_arr[:, 0] = trajectory[:,0]
				for t in range(0, self.T-1):
					dif = x_arr[:,t] - trajectory[:,t]
					dif[3]= np.mod(dif[3] + np.pi, 2*np.pi) - np.pi
					u_arr[:, t] = controls[:, t] + K_arr[:, :, t] @ dif + alpha*k_arr[:, t]
					x_arr[:, t + 1], u_arr[:, t] = self.dyn.integrate_forward_np(x_arr[:, t], u_arr[:, t])

				Jnew = self.cost.get_traj_cost(x_arr, u_arr, path_refs, obs_refs)
				if Jnew <= J:
					if abs(Jnew-J) < self.tol:
						converged = True
					J = Jnew
					trajectory = x_arr
					controls = u_arr
					changed = True
					break
			if converged:
				status = 0
				break
			if not changed:
				status = -1
				print('not changed')
				break
			

		if not converged:
			print('not converged')
			status = -1

		#print('converged')				


		t_process = time.time() - t_start
		solver_info = dict(
				t_process=t_process, # Time spent on planning
				trajectory = trajectory,
				controls = controls,
				status=status, #    TODO: Fill this in
				K_closed_loop=K_arr, # TODO: Fill this in
				k_open_loop=k_arr # TODO: Fill this in
                # Optional TODO: Fill in other information you want to return
        )
		return solver_info

