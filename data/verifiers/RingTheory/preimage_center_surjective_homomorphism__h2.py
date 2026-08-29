import sympy
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class FiniteRing:
    """
    A helper class to define finite rings for the witness.
    """
    def __init__(self, elements, add_func, mul_func, zero):
        self.elements = list(elements)
        self.add_func = add_func
        self.mul_func = mul_func
        self.zero = zero

    def add(self, a, b):
        return self.add_func(a, b)

    def mul(self, a, b):
        return self.mul_func(a, b)

class Witness:
    """
    A helper class to construct the witness.
    """
    def __init__(self, R, S, f, Z_R=None, Z_S=None):
        self.R = R
        self.S = S
        self.f = f
        if Z_R is not None:
            self.Z_R = Z_R
        if Z_S is not None:
            self.Z_S = Z_S

def is_ring(ring):
    try:
        elements = ring.elements
        zero = ring.zero
        if zero not in elements: 
            return False
        
        # Closure
        for a in elements:
            for b in elements:
                if ring.add(a, b) not in elements: return False
                if ring.mul(a, b) not in elements: return False
                
        # Addition commutative and associative
        for a in elements:
            for b in elements:
                if ring.add(a, b) != ring.add(b, a): return False
                for c in elements:
                    if ring.add(ring.add(a, b), c) != ring.add(a, ring.add(b, c)): return False
                    
        # Additive identity
        for a in elements:
            if ring.add(a, zero) != a: return False
            if ring.add(zero, a) != a: return False
            
        # Additive inverse
        for a in elements:
            has_inv = False
            for b in elements:
                if ring.add(a, b) == zero and ring.add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        # Multiplication associative
        for a in elements:
            for b in elements:
                for c in elements:
                    if ring.mul(ring.mul(a, b), c) != ring.mul(a, ring.mul(b, c)): return False
                    
        # Distributive laws
        for a in elements:
            for b in elements:
                for c in elements:
                    if ring.mul(a, ring.add(b, c)) != ring.add(ring.mul(a, b), ring.mul(a, c)): return False
                    if ring.mul(ring.add(a, b), c) != ring.add(ring.mul(a, c), ring.mul(b, c)): return False
                    
        return True
    except Exception:
        return False

def get_center(ring):
    center = []
    for a in ring.elements:
        is_c = True
        for x in ring.elements:
            if ring.mul(a, x) != ring.mul(x, a):
                is_c = False
                break
        if is_c:
            center.append(a)
    return center

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            f = witness['f']
            Z_S_provided = 'Z_S' in witness
            if Z_S_provided: Z_S_val = witness['Z_S']
            Z_R_provided = 'Z_R' in witness
            if Z_R_provided: Z_R_val = witness['Z_R']
        else:
            R = witness.R
            S = witness.S
            f = witness.f
            Z_S_provided = hasattr(witness, 'Z_S')
            if Z_S_provided: Z_S_val = witness.Z_S
            Z_R_provided = hasattr(witness, 'Z_R')
            if Z_R_provided: Z_R_val = witness.Z_R
    except Exception:
        return [False, False, False, False]

    # H1: R and S are rings
    try:
        h1 = is_ring(R) and is_ring(S)
    except Exception:
        h1 = False

    # H2: Z(S) denotes the center of the ring S
    try:
        actual_Z_S = get_center(S)
        if Z_S_provided:
            h2 = len(Z_S_val) == len(actual_Z_S) and all(x in actual_Z_S for x in Z_S_val)
        else:
            h2 = True
    except Exception:
        h2 = False

    # H3: Z(R) denotes the center of the ring R
    try:
        actual_Z_R = get_center(R)
        if Z_R_provided:
            h3 = len(Z_R_val) == len(actual_Z_R) and all(x in actual_Z_R for x in Z_R_val)
        else:
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: The preimage f^{-1}(Z(S)) is NOT a subring of R that contains both Z(R) and ker(f)
    try:
        if isinstance(f, dict):
            f_func = lambda x: f[x]
        else:
            f_func = f
            
        # Verify f maps R to S
        for x in R.elements:
            if f_func(x) not in S.elements:
                return [h1, h2, h3, False]
                
        ker_f = [x for x in R.elements if f_func(x) == S.zero]
        preimage = [x for x in R.elements if f_func(x) in actual_Z_S]
        
        # Check if preimage is a subring of R
        is_subring = True
        if R.zero not in preimage:
            is_subring = False
        else:
            for a in preimage:
                for b in preimage:
                    if R.add(a, b) not in preimage:
                        is_subring = False
                    if R.mul(a, b) not in preimage:
                        is_subring = False
            for a in preimage:
                inv_in_preimage = False
                for b in preimage:
                    if R.add(a, b) == R.zero and R.add(b, a) == R.zero:
                        inv_in_preimage = True
                        break
                if not inv_in_preimage:
                    is_subring = False
                    
        contains_Z_R = all(x in preimage for x in actual_Z_R)
        contains_ker_f = all(x in preimage for x in ker_f)
        
        conclusion = is_subring and contains_Z_R and contains_ker_f
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: Z(S) denotes the center of the ring S",
    "H_3: Z(R) denotes the center of the ring R",
    "¬Q: The preimage f^{-1}(Z(S)) is not a subring of R that contains both Z(R) and ker(f)"
]

N_HYP = 3
NEG_Q_INDEX = 3