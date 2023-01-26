/* This file was automatically generated by CasADi.
   The CasADi copyright holders make no ownership claim of its contents. */
#ifdef __cplusplus
extern "C" {
#endif

/* How to prefix internal symbols */
#ifdef CASADI_CODEGEN_PREFIX
  #define CASADI_NAMESPACE_CONCAT(NS, ID) _CASADI_NAMESPACE_CONCAT(NS, ID)
  #define _CASADI_NAMESPACE_CONCAT(NS, ID) NS ## ID
  #define CASADI_PREFIX(ID) CASADI_NAMESPACE_CONCAT(CODEGEN_PREFIX, ID)
#else
  #define CASADI_PREFIX(ID) traj_planning_kin_cost_ext_cost_fun_jac_hess_ ## ID
#endif

#include <math.h>

#ifndef casadi_real
#define casadi_real double
#endif

#ifndef casadi_int
#define casadi_int int
#endif

/* Add prefix to internal symbols */
#define casadi_f0 CASADI_PREFIX(f0)
#define casadi_s0 CASADI_PREFIX(s0)
#define casadi_s1 CASADI_PREFIX(s1)
#define casadi_s2 CASADI_PREFIX(s2)
#define casadi_s3 CASADI_PREFIX(s3)
#define casadi_s4 CASADI_PREFIX(s4)
#define casadi_s5 CASADI_PREFIX(s5)

/* Symbol visibility in DLLs */
#ifndef CASADI_SYMBOL_EXPORT
  #if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
    #if defined(STATIC_LINKED)
      #define CASADI_SYMBOL_EXPORT
    #else
      #define CASADI_SYMBOL_EXPORT __declspec(dllexport)
    #endif
  #elif defined(__GNUC__) && defined(GCC_HASCLASSVISIBILITY)
    #define CASADI_SYMBOL_EXPORT __attribute__ ((visibility ("default")))
  #else
    #define CASADI_SYMBOL_EXPORT
  #endif
#endif

static const casadi_int casadi_s0[10] = {6, 1, 0, 6, 0, 1, 2, 3, 4, 5};
static const casadi_int casadi_s1[7] = {3, 1, 0, 3, 0, 1, 2};
static const casadi_int casadi_s2[15] = {11, 1, 0, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
static const casadi_int casadi_s3[5] = {1, 1, 0, 1, 0};
static const casadi_int casadi_s4[13] = {9, 1, 0, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8};
static const casadi_int casadi_s5[23] = {9, 9, 0, 1, 2, 2, 5, 8, 8, 8, 8, 11, 0, 1, 3, 4, 8, 3, 4, 8, 3, 4, 8};

/* traj_planning_kin_cost_ext_cost_fun_jac_hess:(i0[6],i1[3],i2[11])->(o0,o1[9],o2[9x9,11nz]) */
static int casadi_f0(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem) {
  casadi_real a0, a1, a10, a11, a12, a13, a14, a15, a16, a17, a18, a2, a3, a4, a5, a6, a7, a8, a9;
  a0=10.;
  a1=arg[2]? arg[2][3] : 0;
  a2=sin(a1);
  a3=arg[0]? arg[0][0] : 0;
  a4=arg[2]? arg[2][0] : 0;
  a5=cos(a1);
  a6=arg[0]? arg[0][5] : 0;
  a7=arg[2]? arg[2][2] : 0;
  a8=(a6-a7);
  a8=(a5*a8);
  a4=(a4+a8);
  a8=(a3-a4);
  a8=(a2*a8);
  a9=cos(a1);
  a10=arg[0]? arg[0][1] : 0;
  a11=arg[2]? arg[2][1] : 0;
  a12=sin(a1);
  a6=(a6-a7);
  a6=(a12*a6);
  a11=(a11+a6);
  a6=(a10-a11);
  a6=(a9*a6);
  a8=(a8-a6);
  a6=(a0*a8);
  a7=(a6*a8);
  a13=100.;
  a14=cos(a1);
  a3=(a3-a4);
  a3=(a14*a3);
  a1=sin(a1);
  a10=(a10-a11);
  a10=(a1*a10);
  a3=(a3+a10);
  a10=(a13*a3);
  a11=(a10*a3);
  a7=(a7+a11);
  a11=arg[1]? arg[1][2] : 0;
  a7=(a7-a11);
  a11=5.0000000000000003e-02;
  a4=arg[1]? arg[1][0] : 0;
  a15=(a11*a4);
  a16=(a15*a4);
  a7=(a7+a16);
  a16=arg[1]? arg[1][1] : 0;
  a17=(a11*a16);
  a18=(a17*a16);
  a7=(a7+a18);
  if (res[0]!=0) res[0][0]=a7;
  a4=(a11*a4);
  a15=(a15+a4);
  if (res[1]!=0) res[1][0]=a15;
  a11=(a11*a16);
  a17=(a17+a11);
  if (res[1]!=0) res[1][1]=a17;
  a17=-1.;
  if (res[1]!=0) res[1][2]=a17;
  a3=(a13*a3);
  a10=(a10+a3);
  a3=(a14*a10);
  a8=(a0*a8);
  a6=(a6+a8);
  a8=(a2*a6);
  a17=(a3+a8);
  if (res[1]!=0) res[1][3]=a17;
  a10=(a1*a10);
  a6=(a9*a6);
  a17=(a10-a6);
  if (res[1]!=0) res[1][4]=a17;
  a17=0.;
  if (res[1]!=0) res[1][5]=a17;
  if (res[1]!=0) res[1][6]=a17;
  if (res[1]!=0) res[1][7]=a17;
  a6=(a6-a10);
  a6=(a12*a6);
  a3=(a3+a8);
  a3=(a5*a3);
  a6=(a6-a3);
  if (res[1]!=0) res[1][8]=a6;
  a6=1.0000000000000001e-01;
  if (res[2]!=0) res[2][0]=a6;
  if (res[2]!=0) res[2][1]=a6;
  a6=(a13*a14);
  a3=(a13*a14);
  a6=(a6+a3);
  a6=(a14*a6);
  a3=(a0*a2);
  a8=(a0*a2);
  a3=(a3+a8);
  a3=(a2*a3);
  a6=(a6+a3);
  if (res[2]!=0) res[2][2]=a6;
  a6=(a13*a1);
  a13=(a13*a1);
  a6=(a6+a13);
  a13=(a14*a6);
  a3=(a0*a9);
  a8=(a0*a9);
  a3=(a3+a8);
  a8=(a2*a3);
  a13=(a13-a8);
  if (res[2]!=0) res[2][3]=a13;
  a8=-200.;
  a14=(a8*a14);
  a10=(a9*a12);
  a17=(a2*a5);
  a10=(a10-a17);
  a17=(a0*a10);
  a0=(a0*a10);
  a17=(a17+a0);
  a2=(a2*a17);
  a0=(a14+a2);
  if (res[2]!=0) res[2][4]=a0;
  if (res[2]!=0) res[2][5]=a13;
  a6=(a1*a6);
  a3=(a9*a3);
  a6=(a6+a3);
  if (res[2]!=0) res[2][6]=a6;
  a8=(a8*a1);
  a9=(a9*a17);
  a17=(a8-a9);
  if (res[2]!=0) res[2][7]=a17;
  if (res[2]!=0) res[2][8]=a0;
  if (res[2]!=0) res[2][9]=a17;
  a9=(a9-a8);
  a12=(a12*a9);
  a14=(a14+a2);
  a5=(a5*a14);
  a12=(a12-a5);
  if (res[2]!=0) res[2][10]=a12;
  return 0;
}

CASADI_SYMBOL_EXPORT int traj_planning_kin_cost_ext_cost_fun_jac_hess(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem){
  return casadi_f0(arg, res, iw, w, mem);
}

CASADI_SYMBOL_EXPORT int traj_planning_kin_cost_ext_cost_fun_jac_hess_alloc_mem(void) {
  return 0;
}

CASADI_SYMBOL_EXPORT int traj_planning_kin_cost_ext_cost_fun_jac_hess_init_mem(int mem) {
  return 0;
}

CASADI_SYMBOL_EXPORT void traj_planning_kin_cost_ext_cost_fun_jac_hess_free_mem(int mem) {
}

CASADI_SYMBOL_EXPORT int traj_planning_kin_cost_ext_cost_fun_jac_hess_checkout(void) {
  return 0;
}

CASADI_SYMBOL_EXPORT void traj_planning_kin_cost_ext_cost_fun_jac_hess_release(int mem) {
}

CASADI_SYMBOL_EXPORT void traj_planning_kin_cost_ext_cost_fun_jac_hess_incref(void) {
}

CASADI_SYMBOL_EXPORT void traj_planning_kin_cost_ext_cost_fun_jac_hess_decref(void) {
}

CASADI_SYMBOL_EXPORT casadi_int traj_planning_kin_cost_ext_cost_fun_jac_hess_n_in(void) { return 3;}

CASADI_SYMBOL_EXPORT casadi_int traj_planning_kin_cost_ext_cost_fun_jac_hess_n_out(void) { return 3;}

CASADI_SYMBOL_EXPORT casadi_real traj_planning_kin_cost_ext_cost_fun_jac_hess_default_in(casadi_int i){
  switch (i) {
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const char* traj_planning_kin_cost_ext_cost_fun_jac_hess_name_in(casadi_int i){
  switch (i) {
    case 0: return "i0";
    case 1: return "i1";
    case 2: return "i2";
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const char* traj_planning_kin_cost_ext_cost_fun_jac_hess_name_out(casadi_int i){
  switch (i) {
    case 0: return "o0";
    case 1: return "o1";
    case 2: return "o2";
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const casadi_int* traj_planning_kin_cost_ext_cost_fun_jac_hess_sparsity_in(casadi_int i) {
  switch (i) {
    case 0: return casadi_s0;
    case 1: return casadi_s1;
    case 2: return casadi_s2;
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const casadi_int* traj_planning_kin_cost_ext_cost_fun_jac_hess_sparsity_out(casadi_int i) {
  switch (i) {
    case 0: return casadi_s3;
    case 1: return casadi_s4;
    case 2: return casadi_s5;
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT int traj_planning_kin_cost_ext_cost_fun_jac_hess_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w) {
  if (sz_arg) *sz_arg = 3;
  if (sz_res) *sz_res = 3;
  if (sz_iw) *sz_iw = 0;
  if (sz_w) *sz_w = 0;
  return 0;
}


#ifdef __cplusplus
} /* extern "C" */
#endif
