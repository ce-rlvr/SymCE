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

CONDITION_LABELS = [
    "H_1: (R_i, phi_ij) is a directed system of rings indexed by a directed set K",
    "H_2: R is the direct limit of the system",
    "¬Q: The kernel of phi_i is NOT given by the union of ker(phi_ij)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_op(op, a, b):
    if callable(op): return op(a, b)
    try:
        return op[(a, b)]
    except KeyError:
        return None

def get_map(f, a):
    if callable(f): return f(a)
    try:
        return f[a]
    except KeyError:
        return None

def is_ring(elements, add, mul, zero):
    if zero not in elements: return False
    # check add abelian group
    for a in elements:
        if get_op(add, a, zero) != a or get_op(add, zero, a) != a: return False
        has_neg = False
        for b in elements:
            if get_op(add, a, b) == zero and get_op(add, b, a) == zero:
                has_neg = True
                break
        if not has_neg: return False
        for b in elements:
            if get_op(add, a, b) != get_op(add, b, a): return False
            for c in elements:
                if get_op(add, get_op(add, a, b), c) != get_op(add, a, get_op(add, b, c)): return False
    # check mul associative
    for a in elements:
        for b in elements:
            for c in elements:
                if get_op(mul, get_op(mul, a, b), c) != get_op(mul, a, get_op(mul, b, c)): return False
    # check distributive
    for a in elements:
        for b in elements:
            for c in elements:
                if get_op(mul, a, get_op(add, b, c)) != get_op(add, get_op(mul, a, b), get_op(mul, a, c)): return False
                if get_op(mul, get_op(add, a, b), c) != get_op(add, get_op(mul, a, c), get_op(mul, b, c)): return False
    return True

def is_homomorphism(elements1, add1, mul1, elements2, add2, mul2, f):
    for a in elements1:
        for b in elements1:
            if get_map(f, get_op(add1, a, b)) != get_op(add2, get_map(f, a), get_map(f, b)): return False
            if get_map(f, get_op(mul1, a, b)) != get_op(mul2, get_map(f, a), get_map(f, b)): return False
    return True

def conditions(witness):
    try:
        K = witness["K"]
        leq = witness["leq"]
        rings = witness["rings"]
        add = witness["add"]
        mul = witness["mul"]
        zero = witness["zero"]
        phi = witness["phi"]
        
        h1 = True
        if not K: h1 = False
        
        # check leq is preorder
        for i in K:
            if (i, i) not in leq: h1 = False
        for i in K:
            for j in K:
                for k in K:
                    if (i, j) in leq and (j, k) in leq:
                        if (i, k) not in leq: h1 = False
        
        # check directed
        for i in K:
            for j in K:
                has_upper = False
                for k in K:
                    if (i, k) in leq and (j, k) in leq:
                        has_upper = True
                        break
                if not has_upper: h1 = False
                
        # check rings
        for i in K:
            if not is_ring(rings[i], add[i], mul[i], zero[i]): h1 = False
            
        # check phi
        for (i, j) in leq:
            if (i, j) not in phi: h1 = False
            else:
                if not is_homomorphism(rings[i], add[i], mul[i], rings[j], add[j], mul[j], phi[(i, j)]): h1 = False
                
        # check functoriality
        for i in K:
            for x in rings[i]:
                if get_map(phi[(i, i)], x) != x: h1 = False
        for i in K:
            for j in K:
                for k in K:
                    if (i, j) in leq and (j, k) in leq:
                        for x in rings[i]:
                            if get_map(phi[(i, k)], x) != get_map(phi[(j, k)], get_map(phi[(i, j)], x)): h1 = False
    except Exception:
        h1 = False

    try:
        R = witness["R"]
        R_add = witness["R_add"]
        R_mul = witness["R_mul"]
        R_zero = witness["R_zero"]
        Phi = witness["Phi"]
        
        h2 = True
        if not is_ring(R, R_add, R_mul, R_zero): h2 = False
        
        for i in K:
            if not is_homomorphism(rings[i], add[i], mul[i], R, R_add, R_mul, Phi[i]): h2 = False
            
        for i in K:
            for j in K:
                if (i, j) in leq:
                    for x in rings[i]:
                        if get_map(Phi[j], get_map(phi[(i, j)], x)) != get_map(Phi[i], x): h2 = False
                        
        # check R is generated by images
        for y in R:
            is_image = False
            for i in K:
                for x in rings[i]:
                    if get_map(Phi[i], x) == y:
                        is_image = True
                        break
                if is_image: break
            if not is_image: h2 = False
            
        # check exactness (injectivity of the canonical map from S to R)
        for i in K:
            for j in K:
                for x in rings[i]:
                    for y in rings[j]:
                        if get_map(Phi[i], x) == get_map(Phi[j], y):
                            equiv = False
                            for k in K:
                                if (i, k) in leq and (j, k) in leq:
                                    if get_map(phi[(i, k)], x) == get_map(phi[(j, k)], y):
                                        equiv = True
                                        break
                            if not equiv: h2 = False
    except Exception:
        h2 = False

    try:
        neg_q = False
        for i in K:
            ker_Phi = []
            for x in rings[i]:
                if get_map(Phi[i], x) == R_zero:
                    ker_Phi.append(x)
                    
            union_ker = []
            for x in rings[i]:
                in_union = False
                for j in K:
                    if (i, j) in leq:
                        if get_map(phi[(i, j)], x) == zero[j]:
                            in_union = True
                            break
                if in_union:
                    union_ker.append(x)
                    
            if set(ker_Phi) != set(union_ker):
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]