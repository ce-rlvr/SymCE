import sympy
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

CONDITION_LABELS = [
    "H_1: (R_i, phi_{ij}) is a directed system of rings indexed by a directed set K",
    "H_2: phi_i: R_i -> R is the canonical ring homomorphism for some i in K",
    "¬Q: The kernel of phi_i is not equal to the union of ker(phi_{ij}) for j >= i"
]
N_HYP = 2
NEG_Q_INDEX = 2

def get_val(obj, *args):
    """Helper to extract values from callables, dicts, or lists."""
    if callable(obj):
        return obj(*args)
    elif isinstance(obj, dict):
        if len(args) == 1:
            return obj[args[0]]
        else:
            return obj[args]
    elif isinstance(obj, list) and len(args) == 1 and isinstance(args[0], int):
        return obj[args[0]]
    else:
        raise TypeError("Cannot extract value")

def is_ring(elements, add, mul, zero, one=None):
    """Checks if the given elements and operations form a ring (or rng)."""
    if zero not in elements: 
        return False
    for x in elements:
        if add(x, zero) != x or add(zero, x) != x: 
            return False
        has_inv = False
        for y in elements:
            if add(x, y) == zero and add(y, x) == zero:
                has_inv = True
                break
        if not has_inv: 
            return False
        for y in elements:
            if add(x, y) != add(y, x): 
                return False
            for z in elements:
                if add(add(x, y), z) != add(x, add(y, z)): return False
                if mul(mul(x, y), z) != mul(x, mul(y, z)): return False
                if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): return False
                if mul(add(x, y), z) != add(mul(x, z), mul(y, z)): return False
    if one is not None:
        if one not in elements: 
            return False
        for x in elements:
            if mul(x, one) != x or mul(one, x) != x: 
                return False
    return True

def conditions(witness):
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        K = list(witness.K)
        if not K:
            raise ValueError
            
        is_directed = True
        for k in K:
            if not get_val(witness.le, k, k): 
                is_directed = False
                break
            for l in K:
                if get_val(witness.le, k, l):
                    for m in K:
                        if get_val(witness.le, l, m) and not get_val(witness.le, k, m): 
                            is_directed = False
                            break
        if is_directed:
            for k in K:
                for l in K:
                    has_upper = False
                    for m in K:
                        if get_val(witness.le, k, m) and get_val(witness.le, l, m):
                            has_upper = True
                            break
                    if not has_upper:
                        is_directed = False
                        break
                if not is_directed: 
                    break
                
        if is_directed:
            H1 = True
            for k in K:
                R_k = list(get_val(witness.R, k))
                one_k = get_val(witness.one, k) if hasattr(witness, 'one') else None
                
                def add_k(x, y, k=k): return get_val(witness.add, k, x, y)
                def mul_k(x, y, k=k): return get_val(witness.mul, k, x, y)
                
                if not is_ring(R_k, add_k, mul_k, get_val(witness.zero, k), one_k):
                    H1 = False
                    break
                for x in R_k:
                    if get_val(witness.phi, k, k, x) != x: 
                        H1 = False
                        break
                if not H1: break
                
                for l in K:
                    if get_val(witness.le, k, l):
                        R_l = list(get_val(witness.R, l))
                        one_l = get_val(witness.one, l) if hasattr(witness, 'one') else None
                        if hasattr(witness, 'one'):
                            if get_val(witness.phi, k, l, one_k) != one_l: 
                                H1 = False
                                break
                        for x in R_k:
                            for y in R_k:
                                if get_val(witness.phi, k, l, add_k(x, y)) != get_val(witness.add, l, get_val(witness.phi, k, l, x), get_val(witness.phi, k, l, y)): 
                                    H1 = False
                                    break
                                if get_val(witness.phi, k, l, mul_k(x, y)) != get_val(witness.mul, l, get_val(witness.phi, k, l, x), get_val(witness.phi, k, l, y)): 
                                    H1 = False
                                    break
                            if not H1: break
                        if not H1: break
                        
                        for m in K:
                            if get_val(witness.le, l, m):
                                for x in R_k:
                                    if get_val(witness.phi, l, m, get_val(witness.phi, k, l, x)) != get_val(witness.phi, k, m, x): 
                                        H1 = False
                                        break
                            if not H1: break
                    if not H1: break
                if not H1: break
    except Exception:
        H1 = False

    try:
        if witness.i in list(witness.K):
            R_target = list(witness.R_target)
            one_t = witness.one_target if hasattr(witness, 'one_target') else None
            
            def add_t(x, y): return get_val(witness.add_target, x, y)
            def mul_t(x, y): return get_val(witness.mul_target, x, y)
            
            if is_ring(R_target, add_t, mul_t, witness.zero_target, one_t):
                H2 = True
                R_i = list(get_val(witness.R, witness.i))
                if hasattr(witness, 'one') and hasattr(witness, 'one_target'):
                    if get_val(witness.phi_i, get_val(witness.one, witness.i)) != witness.one_target:
                        H2 = False
                if H2:
                    for x in R_i:
                        for y in R_i:
                            if get_val(witness.phi_i, get_val(witness.add, witness.i, x, y)) != add_t(get_val(witness.phi_i, x), get_val(witness.phi_i, y)): 
                                H2 = False
                                break
                            if get_val(witness.phi_i, get_val(witness.mul, witness.i, x, y)) != mul_t(get_val(witness.phi_i, x), get_val(witness.phi_i, y)): 
                                H2 = False
                                break
                        if not H2: break
    except Exception:
        H2 = False

    try:
        i = witness.i
        R_i = list(get_val(witness.R, i))
        K = list(witness.K)
        
        ker_phi_i = []
        for x in R_i:
            if get_val(witness.phi_i, x) == witness.zero_target:
                if x not in ker_phi_i:
                    ker_phi_i.append(x)
                    
        union_ker_phi_ij = []
        for x in R_i:
            for j in K:
                if get_val(witness.le, i, j):
                    if get_val(witness.phi, i, j, x) == get_val(witness.zero, j):
                        if x not in union_ker_phi_ij:
                            union_ker_phi_ij.append(x)
                        break
                        
        neg_Q = False
        for x in ker_phi_i:
            if x not in union_ker_phi_ij:
                neg_Q = True
                break
        if not neg_Q:
            for x in union_ker_phi_ij:
                if x not in ker_phi_i:
                    neg_Q = True
                    break
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]