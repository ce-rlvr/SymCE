import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R and S are valid rings",
    "H_2: f is a surjective ring homomorphism from R to S",
    "¬Q: The image f(Z(R)) is NOT contained in the center of S"
]

def eq(a, b):
    if hasattr(a, 'equals') and callable(a.equals):
        try:
            res = a.equals(b)
            if res is not None: return res
        except Exception:
            pass
    return a == b

def conditions(witness):
    # Try table format first: (R_add, R_mul, S_add, S_mul, f_map)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 5:
            R_add, R_mul, S_add, S_mul, f_map = witness
            if isinstance(R_add, (list, tuple)) and len(R_add) > 0 and isinstance(R_add[0], (list, tuple)):
                
                def is_ring_t(add_t, mul_t):
                    n = len(add_t)
                    if n == 0: return False
                    if len(mul_t) != n: return False
                    for row in list(add_t) + list(mul_t):
                        if len(row) != n: return False
                        for val in row:
                            if not isinstance(val, int) or not (0 <= val < n): return False
                    for i in range(n):
                        for j in range(n):
                            for k in range(n):
                                if add_t[add_t[i][j]][k] != add_t[i][add_t[j][k]]: return False
                                if mul_t[mul_t[i][j]][k] != mul_t[i][mul_t[j][k]]: return False
                                if mul_t[i][add_t[j][k]] != add_t[mul_t[i][j]][mul_t[i][k]]: return False
                                if mul_t[add_t[i][j]][k] != add_t[mul_t[i][k]][mul_t[j][k]]: return False
                            if add_t[i][j] != add_t[j][i]: return False
                    has_zero = False
                    for z in range(n):
                        if all(add_t[z][i] == i for i in range(n)):
                            has_zero = True
                            for i in range(n):
                                if not any(add_t[i][j] == z for j in range(n)): return False
                            break
                    return has_zero

                h1 = is_ring_t(R_add, R_mul) and is_ring_t(S_add, S_mul)
                
                n = len(R_add)
                m = len(S_add)
                h2 = False
                if isinstance(f_map, (list, tuple)) and len(f_map) == n:
                    is_hom = True
                    for i in range(n):
                        if not isinstance(f_map[i], int) or not (0 <= f_map[i] < m):
                            is_hom = False
                            break
                        for j in range(n):
                            if f_map[R_add[i][j]] != S_add[f_map[i]][f_map[j]]:
                                is_hom = False
                                break
                            if f_map[R_mul[i][j]] != S_mul[f_map[i]][f_map[j]]:
                                is_hom = False
                                break
                        if not is_hom: break
                    is_surj = len(set(f_map)) == m
                    h2 = is_hom and is_surj
                    
                def get_center_t(mul_t):
                    n = len(mul_t)
                    return [i for i in range(n) if all(mul_t[i][j] == mul_t[j][i] for j in range(n))]
                    
                Z_R = get_center_t(R_mul)
                Z_S = set(get_center_t(S_mul))
                
                if isinstance(f_map, (list, tuple)) and len(f_map) == n:
                    f_Z_R = set(f_map[x] for x in Z_R)
                    neg_q = not f_Z_R.issubset(Z_S)
                else:
                    neg_q = False
                
                return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # Try object format: (R_elements, S_elements, f_mapping)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            R_obj, S_obj, f = witness
            
            R = []
            for x in R_obj:
                R.append(x)
                if len(R) > 30:
                    return [False, False, False]
                    
            S = []
            for x in S_obj:
                S.append(x)
                if len(S) > 30:
                    return [False, False, False]
                    
            f_func = (lambda x: f[x]) if isinstance(f, dict) else f
            
            def is_ring_o(ring):
                if not ring: return False
                zero = None
                for z in ring:
                    if all(eq(x + z, x) for x in ring):
                        zero = z
                        break
                if zero is None: return False
                for x in ring:
                    if not any(eq(x + y, zero) for y in ring): return False
                    for y in ring:
                        try:
                            xy_add = x + y
                            xy_mul = x * y
                        except Exception:
                            return False
                        if not any(eq(xy_add, r) for r in ring): return False
                        if not any(eq(xy_mul, r) for r in ring): return False
                        if not eq(xy_add, y + x): return False
                        for z in ring:
                            try:
                                if not eq(xy_add + z, x + (y + z)): return False
                                if not eq(xy_mul * z, x * (y * z)): return False
                                if not eq(x * (y + z), xy_mul + x * z): return False
                                if not eq((x + y) * z, x * z + y * z): return False
                            except Exception:
                                return False
                return True
                
            h1 = is_ring_o(R) and is_ring_o(S)
            
            is_hom = True
            mapped = []
            for x in R:
                try:
                    fx = f_func(x)
                except Exception:
                    is_hom = False
                    break
                if not any(eq(fx, s) for s in S):
                    is_hom = False
                    break
                mapped.append(fx)
                for y in R:
                    try:
                        if not eq(f_func(x + y), fx + f_func(y)):
                            is_hom = False
                            break
                        if not eq(f_func(x * y), fx * f_func(y)):
                            is_hom = False
                            break
                    except Exception:
                        is_hom = False
                        break
                if not is_hom: break
                
            is_surj = False
            if is_hom:
                uncovered = list(S)
                for mx in mapped:
                    for u in uncovered:
                        if eq(mx, u):
                            uncovered.remove(u)
                            break
                is_surj = len(uncovered) == 0
                
            h2 = is_hom and is_surj
            
            def get_center_o(ring):
                center = []
                for x in ring:
                    is_c = True
                    for y in ring:
                        try:
                            if not eq(x * y, y * x):
                                is_c = False
                                break
                        except Exception:
                            is_c = False
                            break
                    if is_c:
                        center.append(x)
                return center
                
            Z_R = get_center_o(R)
            Z_S = get_center_o(S)
            
            f_Z_R = []
            for x in Z_R:
                try:
                    f_Z_R.append(f_func(x))
                except Exception:
                    pass
                    
            is_subset = True
            for fz in f_Z_R:
                if not any(eq(fz, zs) for zs in Z_S):
                    is_subset = False
                    break
                    
            neg_q = not is_subset
            
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass
        
    return [False, False, False]