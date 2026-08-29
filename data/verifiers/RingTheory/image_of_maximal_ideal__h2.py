import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: Standard finite rings for the witness to use
def make_Zn(n):
    elements = list(range(n))
    add = {(i, j): (i + j) % n for i in elements for j in elements}
    mul = {(i, j): (i * j) % n for i in elements for j in elements}
    return (elements, add, mul)

def make_product_ring(R1, R2):
    E1, A1, M1 = R1
    E2, A2, M2 = R2
    elements = [(e1, e2) for e1 in E1 for e2 in E2]
    add = {((a1, a2), (b1, b2)): (A1[(a1, b1)], A2[(a2, b2)]) for a1 in E1 for a2 in E2 for b1 in E1 for b2 in E2}
    mul = {((a1, a2), (b1, b2)): (M1[(a1, b1)], M2[(a2, b2)]) for a1 in E1 for a2 in E2 for b1 in E1 for b2 in E2}
    return (elements, add, mul)

Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z6 = make_Zn(6)
Z2xZ2 = make_product_ring(Z2, Z2)

def get_val(op, a, b):
    if callable(op): return op(a, b)
    try: return op[(a, b)]
    except (KeyError, TypeError): pass
    return op[a][b]

def normalize_ring(R):
    elements, add, mul = R
    elements = list(elements)
    add_dict = {}
    mul_dict = {}
    for a in elements:
        for b in elements:
            add_dict[(a,b)] = get_val(add, a, b)
            mul_dict[(a,b)] = get_val(mul, a, b)
    return elements, add_dict, mul_dict

def is_commutative_ring(R):
    try:
        elements, add, mul = R
        
        for a in elements:
            for b in elements:
                if add.get((a,b)) not in elements: return False
                if mul.get((a,b)) not in elements: return False
                
        for a in elements:
            for b in elements:
                if add[(a,b)] != add[(b,a)]: return False
                if mul[(a,b)] != mul[(b,a)]: return False
                
        for a in elements:
            for b in elements:
                for c in elements:
                    if add[(a, add[(b,c)])] != add[(add[(a,b)], c)]: return False
                    if mul[(a, mul[(b,c)])] != mul[(mul[(a,b)], c)]: return False
                    
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul[(a, add[(b,c)])] != add[(mul[(a,b)], mul[(a,c)])]: return False
                    
        zeros = [z for z in elements if all(add[(a,z)] == a for a in elements)]
        if len(zeros) != 1: return False
        z = zeros[0]
        
        for a in elements:
            if not any(add[(a,b)] == z for b in elements): return False
            
        ones = [u for u in elements if all(mul[(a,u)] == a for a in elements)]
        if len(ones) != 1: return False
        
        return True
    except Exception:
        return False

def is_ideal(R, I):
    try:
        elements, add, mul = R
        I_list = list(I)
        if not I_list: return False
        if any(x not in elements for x in I_list): return False
        
        zeros = [z for z in elements if all(add[(a,z)] == a for a in elements)]
        if not zeros: return False
        z = zeros[0]
        if z not in I_list: return False
        
        for a in I_list:
            for b in I_list:
                if add[(a,b)] not in I_list: return False
                
        for a in I_list:
            inv_a = [b for b in elements if add[(a,b)] == z]
            if not inv_a or inv_a[0] not in I_list: return False
            
        for a in I_list:
            for r in elements:
                if mul[(a,r)] not in I_list: return False
                if mul[(r,a)] not in I_list: return False
                
        return True
    except Exception:
        return False

def is_maximal_ideal(R, I):
    try:
        elements, add, mul = R
        if not is_ideal(R, I): return False
        
        I_list = list(I)
        if all(e in I_list for e in elements): return False
        
        for x in elements:
            if x in I_list: continue
            
            gen = []
            for i in I_list:
                for r in elements:
                    val = add[(i, mul[(r, x)])]
                    if val not in gen:
                        gen.append(val)
            
            if not all(e in gen for e in elements):
                return False
                
        return True
    except Exception:
        return False

def is_homomorphism(R, S, f):
    try:
        R_elem, R_add, R_mul = R
        S_elem, S_add, S_mul = S
        
        if any(x not in f for x in R_elem): return False
        if any(f[x] not in S_elem for x in R_elem): return False
        
        for a in R_elem:
            for b in R_elem:
                if f[R_add[(a,b)]] != S_add[(f[a], f[b])]: return False
                if f[R_mul[(a,b)]] != S_mul[(f[a], f[b])]: return False
                
        R_ones = [u for u in R_elem if all(R_mul[(a,u)] == a for a in R_elem)]
        S_ones = [u for u in S_elem if all(S_mul[(a,u)] == a for a in S_elem)]
        if R_ones and S_ones:
            if f[R_ones[0]] != S_ones[0]: return False
            
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        R_raw = witness['R']
        S_raw = witness['S']
        M = list(witness['M'])
        f_raw = witness['f']
        
        R = normalize_ring(R_raw)
        S = normalize_ring(S_raw)
        
        R_elem = R[0]
        f = {}
        for x in R_elem:
            if callable(f_raw):
                f[x] = f_raw(x)
            elif isinstance(f_raw, dict):
                f[x] = f_raw[x]
            else:
                f[x] = f_raw[x]
                
        h1 = is_commutative_ring(R) and is_commutative_ring(S) and is_homomorphism(R, S, f)
        h2 = is_maximal_ideal(R, M)
        
        S_elem, S_add, S_mul = S
        S_zeros = [z for z in S_elem if all(S_add[(a,z)] == a for a in S_elem)]
        if not S_zeros:
            h3 = False
        else:
            S_zero = S_zeros[0]
            ker_f = [x for x in R_elem if f[x] == S_zero]
            h3 = all(x in M for x in ker_f)
            
        f_M = []
        for x in M:
            if f[x] not in f_M:
                f_M.append(f[x])
                
        neg_q = not is_maximal_ideal(S, f_M)
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings and f is a ring homomorphism from R to S",
    "H_2: M is a maximal ideal of R",
    "H_3: The kernel of f is contained in M",
    "¬Q: The image f(M) is not a maximal ideal of S"
]

N_HYP = 3
NEG_Q_INDEX = 3