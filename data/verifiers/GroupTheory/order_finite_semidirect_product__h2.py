import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (N, H, phi) where:
      - N and H are finite groups (e.g., SymPy PermutationGroup objects)
      - phi is a callable or dict mapping H x N -> N
    """
    try:
        N, H, phi = witness
    except Exception:
        return [False, False, False]
        
    # H_1: N is a finite group
    try:
        try:
            N_elems = list(N.generate())
        except Exception:
            N_elems = list(N.elements)
        h1_ok = len(N_elems) > 0
    except Exception:
        h1_ok = False
        
    # H_2: H is a finite group
    try:
        try:
            H_elems = list(H.generate())
        except Exception:
            H_elems = list(H.elements)
        h2_ok = len(H_elems) > 0
    except Exception:
        h2_ok = False
        
    # ¬Q: The external semidirect product N ⋊_φ H is not a finite group of order |N| × |H|
    try:
        if not (h1_ok and h2_ok):
            return [h1_ok, h2_ok, False]
            
        def get_phi_val(phi, h, n):
            if callable(phi):
                return phi(h, n)
            elif isinstance(phi, dict):
                if (h, n) in phi:
                    return phi[(h, n)]
                else:
                    return phi[h][n]
            else:
                raise ValueError("phi must be callable or dict")
                
        # Verify phi is a valid map H x N -> N
        for h in H_elems:
            for n in N_elems:
                if get_phi_val(phi, h, n) not in N_elems:
                    return [h1_ok, h2_ok, False]
                    
        elements = [(n, h) for n in N_elems for h in H_elems]
        
        def op(x, y):
            n1, h1 = x
            n2, h2 = y
            # Operation: (n1, h1) * (n2, h2) = (n1 * phi_{h1}(n2), h1 * h2)
            return (n1 * get_phi_val(phi, h1, n2), h1 * h2)
            
        is_group = True
        
        # Check closure
        for a in elements:
            for b in elements:
                c = op(a, b)
                if c not in elements:
                    is_group = False
                    break
            if not is_group:
                break
                
        # Check associativity
        if is_group:
            for a in elements:
                for b in elements:
                    for c in elements:
                        if op(op(a, b), c) != op(a, op(b, c)):
                            is_group = False
                            break
                    if not is_group:
                        break
                if not is_group:
                    break
                    
        # Check identity
        if is_group:
            identity = None
            for e in elements:
                is_id = True
                for a in elements:
                    if op(e, a) != a or op(a, e) != a:
                        is_id = False
                        break
                if is_id:
                    identity = e
                    break
            if identity is None:
                is_group = False
                
        # Check inverses
        if is_group:
            for a in elements:
                has_inv = False
                for b in elements:
                    if op(a, b) == identity and op(b, a) == identity:
                        has_inv = True
                        break
                if not has_inv:
                    is_group = False
                    break
                    
        neg_q_ok = not is_group
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a finite group",
    "H_2: H is a finite group",
    "¬Q: The external semidirect product N ⋊_φ H is not a finite group of order |N| × |H|"
]

N_HYP = 2
NEG_Q_INDEX = 2