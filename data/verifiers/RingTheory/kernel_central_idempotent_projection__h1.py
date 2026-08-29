import sympy
from sympy import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import functools
import math

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    try:
        R, e = witness
    except Exception:
        return [False, False, False]
    
    # Validate that R is a ring-like structure (closed under +, -, *)
    try:
        if not isinstance(R, list) or len(R) == 0:
            return [False, False, False]
        
        closed = True
        for x in R:
            if not closed: break
            for y in R:
                if not any(x + y == z for z in R): 
                    closed = False
                    break
                if not any(x * y == z for z in R): 
                    closed = False
                    break
                if not any(x - y == z for z in R): 
                    closed = False
                    break
        if not closed:
            return [False, False, False]
            
        zero = None
        for z in R:
            is_z = True
            for x in R:
                if z + x != x:
                    is_z = False
                    break
            if is_z:
                zero = z
                break
        if zero is None:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    # H_1: e is a central idempotent element of R
    h1 = False
    try:
        if any(e == x for x in R):
            central = True
            for x in R:
                if e * x != x * e:
                    central = False
                    break
            idempotent = (e * e == e)
            if central and idempotent:
                h1 = True
    except Exception:
        h1 = False

    # H_2: f: R -> eRe is the map defined by f(x) = ex
    h2 = False
    try:
        eRe = []
        for x in R:
            eRe.append(e * x * e)
        maps_into = True
        for x in R:
            if not any(e * x == y for y in eRe):
                maps_into = False
                break
        if maps_into:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The map f is NOT a surjective ring homomorphism OR its kernel is NOT the ideal (1-e)R
    neg_q = False
    try:
        ident = None
        for x in R:
            is_id = True
            for y in R:
                if x * y != y or y * x != y:
                    is_id = False
                    break
            if is_id:
                ident = x
                break
        
        is_hom = True
        for x in R:
            if not is_hom: break
            for y in R:
                if e * (x + y) != (e * x) + (e * y):
                    is_hom = False
                    break
                if e * (x * y) != (e * x) * (e * y):
                    is_hom = False
                    break
        
        is_surj = True
        for y in eRe:
            if not any(e * x == y for x in R):
                is_surj = False
                break
        
        if not is_hom or not is_surj:
            neg_q = True
        elif ident is None:
            # R has no multiplicative identity, so the ideal (1-e)R is undefined
            neg_q = True
        else:
            one_minus_e = ident - e
            if not any(one_minus_e == x for x in R):
                neg_q = True
            else:
                ideal = []
                for x in R:
                    ideal.append(one_minus_e * x)
                
                kernel = []
                for x in R:
                    if e * x == zero:
                        kernel.append(x)
                
                ideal_subset_kernel = True
                for i in ideal:
                    if not any(i == k for k in kernel):
                        ideal_subset_kernel = False
                        break
                        
                kernel_subset_ideal = True
                for k in kernel:
                    if not any(k == i for i in ideal):
                        kernel_subset_ideal = False
                        break
                
                if not (ideal_subset_kernel and kernel_subset_ideal):
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: e is a central idempotent element of R",
    "H_2: f: R -> eRe is the map defined by f(x) = ex",
    "¬Q: f is not a surjective ring homomorphism or its kernel is not the ideal (1-e)R"
]

N_HYP = 2
NEG_Q_INDEX = 2