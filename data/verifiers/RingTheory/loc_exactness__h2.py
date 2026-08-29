import sympy
from sympy import *
import itertools
import functools
import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def apply_op(op, *args):
    if isinstance(op, dict):
        return op[args]
    else:
        return op(*args)

def check_H1(w):
    try:
        R = list(w['R'])
        add = w['R_add']
        mul = w['R_mul']
        z = w['R_zero']
        one = w['R_one']
        
        if z not in R or one not in R: return False
        
        for a in R:
            if apply_op(add, a, z) != a: return False
            if apply_op(add, z, a) != a: return False
            if apply_op(mul, a, one) != a: return False
            if apply_op(mul, one, a) != a: return False
            
            has_inv = False
            for b in R:
                if apply_op(add, a, b) == z and apply_op(add, b, a) == z:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in R:
                if apply_op(add, a, b) not in R: return False
                if apply_op(mul, a, b) not in R: return False
                if apply_op(add, a, b) != apply_op(add, b, a): return False
                if apply_op(mul, a, b) != apply_op(mul, b, a): return False
                
                for c in R:
                    if apply_op(add, apply_op(add, a, b), c) != apply_op(add, a, apply_op(add, b, c)): return False
                    if apply_op(mul, apply_op(mul, a, b), c) != apply_op(mul, a, apply_op(mul, b, c)): return False
                    if apply_op(mul, a, apply_op(add, b, c)) != apply_op(add, apply_op(mul, a, b), apply_op(mul, a, c)): return False
                    
        return True
    except Exception:
        return False

def check_module(M, add, action, z, R, R_add, R_mul, R_one):
    M = list(M)
    R = list(R)
    if z not in M: return False
    for m in M:
        if apply_op(add, m, z) != m: return False
        if apply_op(add, z, m) != m: return False
        if apply_op(action, R_one, m) != m: return False
        
        has_inv = False
        for n in M:
            if apply_op(add, m, n) == z and apply_op(add, n, m) == z:
                has_inv = True
                break
        if not has_inv: return False
        
        for n in M:
            if apply_op(add, m, n) not in M: return False
            if apply_op(add, m, n) != apply_op(add, n, m): return False
            for p in M:
                if apply_op(add, apply_op(add, m, n), p) != apply_op(add, m, apply_op(add, n, p)): return False
                
    for r in R:
        for m in M:
            if apply_op(action, r, m) not in M: return False
            for n in M:
                if apply_op(action, r, apply_op(add, m, n)) != apply_op(add, apply_op(action, r, m), apply_op(action, r, n)): return False
        for s in R:
            for m in M:
                if apply_op(action, apply_op(R_add, r, s), m) != apply_op(add, apply_op(action, r, m), apply_op(action, s, m)): return False
                if apply_op(action, apply_op(R_mul, r, s), m) != apply_op(action, r, apply_op(action, s, m)): return False
    return True

def check_H2(w):
    try:
        R = list(w['R'])
        R_add = w['R_add']
        R_mul = w['R_mul']
        R_one = w['R_one']
        
        Mp = list(w['M_prime'])
        M = list(w['M'])
        Mdp = list(w['M_double_prime'])
        
        if not check_module(Mp, w['Mp_add'], w['Mp_action'], w['Mp_zero'], R, R_add, R_mul, R_one): return False
        if not check_module(M, w['M_add'], w['M_action'], w['M_zero'], R, R_add, R_mul, R_one): return False
        if not check_module(Mdp, w['Mdp_add'], w['Mdp_action'], w['Mdp_zero'], R, R_add, R_mul, R_one): return False
        
        f = w['f']
        g = w['g']
        
        for r in R:
            for m1 in Mp:
                for m2 in Mp:
                    if apply_op(f, apply_op(w['Mp_add'], m1, m2)) != apply_op(w['M_add'], apply_op(f, m1), apply_op(f, m2)): return False
                if apply_op(f, apply_op(w['Mp_action'], r, m1)) != apply_op(w['M_action'], r, apply_op(f, m1)): return False
                
        for r in R:
            for m1 in M:
                for m2 in M:
                    if apply_op(g, apply_op(w['M_add'], m1, m2)) != apply_op(w['Mdp_add'], apply_op(g, m1), apply_op(g, m2)): return False
                if apply_op(g, apply_op(w['M_action'], r, m1)) != apply_op(w['Mdp_action'], r, apply_op(g, m1)): return False
                
        for m in Mp:
            if apply_op(f, m) == w['M_zero'] and m != w['Mp_zero']: return False
            
        im_g = []
        for m in M:
            val = apply_op(g, m)
            if val not in im_g:
                im_g.append(val)
        for mdp in Mdp:
            if mdp not in im_g: return False
            
        im_f = []
        for m in Mp:
            val = apply_op(f, m)
            if val not in im_f:
                im_f.append(val)
                
        ker_g = []
        for m in M:
            if apply_op(g, m) == w['Mdp_zero']:
                ker_g.append(m)
                
        for x in im_f:
            if x not in ker_g: return False
        for x in ker_g:
            if x not in im_f: return False
            
        return True
    except Exception:
        return False

def is_localized_exact(w):
    S = list(w['S'])
    Mp = list(w['M_prime'])
    M = list(w['M'])
    Mdp = list(w['M_double_prime'])
    f = w['f']
    g = w['g']
    Mp_action = w['Mp_action']
    M_action = w['M_action']
    Mdp_action = w['Mdp_action']
    Mp_zero = w['Mp_zero']
    M_zero = w['M_zero']
    Mdp_zero = w['Mdp_zero']
    
    for mp in Mp:
        t_exists = False
        for t in S:
            if apply_op(f, apply_op(Mp_action, t, mp)) == M_zero:
                t_exists = True
                break
        if t_exists:
            u_exists = False
            for u in S:
                if apply_op(Mp_action, u, mp) == Mp_zero:
                    u_exists = True
                    break
            if not u_exists: return False
            
    for mp in Mp:
        t_exists = False
        val = apply_op(g, apply_op(f, mp))
        for t in S:
            if apply_op(Mdp_action, t, val) == Mdp_zero:
                t_exists = True
                break
        if not t_exists: return False
        
    for m in M:
        t_exists = False
        for t in S:
            if apply_op(g, apply_op(M_action, t, m)) == Mdp_zero:
                t_exists = True
                break
        if t_exists:
            v_exists = False
            for v in S:
                vm = apply_op(M_action, v, m)
                for mp in Mp:
                    if vm == apply_op(f, mp):
                        v_exists = True
                        break
                if v_exists: break
            if not v_exists: return False
            
    for mdp in Mdp:
        v_exists = False
        for v in S:
            vmdp = apply_op(Mdp_action, v, mdp)
            for m in M:
                if vmdp == apply_op(g, m):
                    v_exists = True
                    break
            if v_exists: break
        if not v_exists: return False
        
    return True

def check_neg_Q(w):
    try:
        S = list(w['S'])
        R = list(w['R'])
        if len(S) == 0:
            return True
        for s in S:
            if s not in R:
                return True
        R_mul = w['R_mul']
        for s1 in S:
            for s2 in S:
                if apply_op(R_mul, s1, s2) not in S:
                    return True
                    
        return not is_localized_exact(w)
    except Exception:
        return False

def conditions(witness):
    return [check_H1(witness), check_H2(witness), check_neg_Q(witness)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: 0 -> M' -> M -> M'' -> 0 is a short exact sequence of R-modules",
    "¬Q: The induced sequence 0 -> S^{-1}M' -> S^{-1}M -> S^{-1}M'' -> 0 is not a short exact sequence of S^{-1}R-modules"
]

N_HYP = 2
NEG_Q_INDEX = 2