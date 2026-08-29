import sympy
from sympy import simplify, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def eq(a, b):
    if a == b: return True
    try:
        diff = a - b
        if hasattr(diff, 'is_zero') and diff.is_zero: return True
        if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix: return True
        if simplify(diff) == 0: return True
    except Exception:
        pass
    return False

def in_set(a, S):
    return any(eq(a, s) for s in S)

def get_ops(witness):
    if isinstance(witness, dict):
        if 'R_add' in witness:
            R = list(range(len(witness['R_add'])))
            S = list(range(len(witness['S_add'])))
            def aR(x, y): return witness['R_add'][x][y]
            def mR(x, y): return witness['R_mul'][x][y]
            def aS(x, y): return witness['S_add'][x][y]
            def mS(x, y): return witness['S_mul'][x][y]
            f_map = witness['f']
            def f(x): return f_map[x] if isinstance(f_map, (list, tuple, dict)) else f_map(x)
            I = witness['I']
            return R, S, aR, mR, aS, mS, f, I
        elif 'n' in witness and 'm' in witness:
            n = witness['n']
            m = witness['m']
            R = list(range(n))
            S = list(range(m))
            def aR(x, y): return (x + y) % n
            def mR(x, y): return (x * y) % n
            def aS(x, y): return (x + y) % m
            def mS(x, y): return (x * y) % m
            f_map = witness['f']
            def f(x): return f_map[x] if isinstance(f_map, (list, tuple, dict)) else f_map(x)
            I = witness['I']
            return R, S, aR, mR, aS, mS, f, I
        elif 'R' in witness:
            R = list(witness['R'])
            S = list(witness['S'])
            f_map = witness['f']
            I = list(witness['I'])
            def aR(x, y): return x + y
            def mR(x, y): return x * y
            def aS(x, y): return x + y
            def mS(x, y): return x * y
            def f(x):
                if isinstance(f_map, dict): return f_map[x]
                if isinstance(f_map, (list, tuple)):
                    for idx, r in enumerate(R):
                        if eq(r, x): return f_map[idx]
                    raise ValueError("x not in R")
                return f_map(x)
            return R, S, aR, mR, aS, mS, f, I
    elif isinstance(witness, tuple):
        if len(witness) == 4:
            if isinstance(witness[0], int) and isinstance(witness[1], int):
                n, m, f_map, I = witness
                R = list(range(n))
                S = list(range(m))
                def aR(x, y): return (x + y) % n
                def mR(x, y): return (x * y) % n
                def aS(x, y): return (x + y) % m
                def mS(x, y): return (x * y) % m
                def f(x):
                    if isinstance(f_map, dict): return f_map[x]
                    if isinstance(f_map, (list, tuple)): return f_map[x]
                    return f_map(x)
                return R, S, aR, mR, aS, mS, f, list(I)
            else:
                R, S, f_map, I = witness
                R = list(R)
                S = list(S)
                I = list(I)
                def aR(x, y): return x + y
                def mR(x, y): return x * y
                def aS(x, y): return x + y
                def mS(x, y): return x * y
                def f(x):
                    if isinstance(f_map, dict): return f_map[x]
                    if isinstance(f_map, (list, tuple)):
                        for idx, r in enumerate(R):
                            if eq(r, x): return f_map[idx]
                        raise ValueError("x not in R")
                    return f_map(x)
                return R, S, aR, mR, aS, mS, f, I
        elif len(witness) == 6:
            R_add, R_mul, S_add, S_mul, f_map, I = witness
            R = list(range(len(R_add)))
            S = list(range(len(S_add)))
            def aR(x, y): return R_add[x][y]
            def mR(x, y): return R_mul[x][y]
            def aS(x, y): return S_add[x][y]
            def mS(x, y): return S_mul[x][y]
            def f(x): return f_map[x] if isinstance(f_map, (list, tuple, dict)) else f_map(x)
            return R, S, aR, mR, aS, mS, f, I
    raise ValueError("Unknown format")

def is_ring(R, add, mul):
    if not R: return False
    for x in R:
        for y in R:
            if not in_set(add(x, y), R): return False
            if not in_set(mul(x, y), R): return False
    for x in R:
        for y in R:
            if not eq(add(x, y), add(y, x)): return False
    for x in R:
        for y in R:
            for z in R:
                if not eq(add(add(x, y), z), add(x, add(y, z))): return False
                if not eq(mul(mul(x, y), z), mul(x, mul(y, z))): return False
                if not eq(mul(x, add(y, z)), add(mul(x, y), mul(x, z))): return False
                if not eq(mul(add(x, y), z), add(mul(x, z), mul(y, z))): return False
    zero = None
    for z in R:
        if all(eq(add(z, x), x) for x in R):
            zero = z
            break
    if zero is None: return False
    for x in R:
        if not any(eq(add(x, y), zero) for y in R):
            return False
    return True

def is_homomorphism(R, S, add_R, mul_R, add_S, mul_S, f):
    for x in R:
        if not in_set(f(x), S): return False
    for x in R:
        for y in R:
            if not eq(f(add_R(x, y)), add_S(f(x), f(y))): return False
            if not eq(f(mul_R(x, y)), mul_S(f(x), f(y))): return False
    return True

def neg_Q_eval(R, S, add_R, mul_R, add_S, mul_S, f, I):
    for i in I:
        if not in_set(i, R): return False
        
    zero_S = None
    for z in S:
        if all(eq(add_S(z, x), x) for x in S):
            zero_S = z
            break
    if zero_S is None: return False
    
    ker = [x for x in R if eq(f(x), zero_S)]
    
    I_plus_ker = []
    for i in I:
        for k in ker:
            s = add_R(i, k)
            if not in_set(s, I_plus_ker):
                I_plus_ker.append(s)
                
    f_I = []
    for i in I:
        fi = f(i)
        if not in_set(fi, f_I):
            f_I.append(fi)
            
    f_inv = []
    for x in R:
        if in_set(f(x), f_I):
            f_inv.append(x)
            
    is_ideal_flag = True
    zero_R = None
    for z in R:
        if all(eq(add_R(z, x), x) for x in R):
            zero_R = z
            break
            
    if not in_set(zero_R, I_plus_ker):
        is_ideal_flag = False
    else:
        for x in I_plus_ker:
            for y in I_plus_ker:
                if not in_set(add_R(x, y), I_plus_ker):
                    is_ideal_flag = False
                    break
            if not is_ideal_flag: break
            
        if is_ideal_flag:
            for x in I_plus_ker:
                has_inv = False
                for y in R:
                    if eq(add_R(x, y), zero_R) and in_set(y, I_plus_ker):
                        has_inv = True
                        break
                if not has_inv:
                    is_ideal_flag = False
                    break
                    
        if is_ideal_flag:
            for x in I_plus_ker:
                for r in R:
                    if not in_set(mul_R(r, x), I_plus_ker):
                        is_ideal_flag = False
                        break
                    if not in_set(mul_R(x, r), I_plus_ker):
                        is_ideal_flag = False
                        break
                if not is_ideal_flag: break

    eq_flag = True
    for x in f_inv:
        if not in_set(x, I_plus_ker):
            eq_flag = False
            break
    if eq_flag:
        for x in I_plus_ker:
            if not in_set(x, f_inv):
                eq_flag = False
                break
                
    return not (is_ideal_flag and eq_flag)

def conditions(witness):
    try:
        R, S, add_R, mul_R, add_S, mul_S, f, I = get_ops(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_ring(R, add_R, mul_R) and is_ring(S, add_S, mul_S)
    except Exception:
        h1 = False
        
    try:
        h2 = is_homomorphism(R, S, add_R, mul_R, add_S, mul_S, f)
    except Exception:
        h2 = False
        
    try:
        nq = neg_Q_eval(R, S, add_R, mul_R, add_S, mul_S, f, I)
    except Exception:
        nq = False
        
    return [h1, h2, nq]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a ring homomorphism from R to S",
    "¬Q: The preimage f^{-1}(f(I)) is not equal to the ideal I + \ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2