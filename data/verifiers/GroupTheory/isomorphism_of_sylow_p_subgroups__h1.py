import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy import isprime, oo
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, evaluates the remaining hypotheses and the negated conclusion.
    The witness is expected to provide p, G, P, Q (e.g., as a tuple, dict, or object attributes).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            p, G, P, Q = witness
        elif isinstance(witness, dict):
            p, G, P, Q = witness['p'], witness['G'], witness['P'], witness['Q']
        else:
            p, G, P, Q = witness.p, witness.G, witness.P, witness.Q
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: P and Q are Sylow p-subgroups of G
    def check_sylow(H, G, p):
        try:
            # Check if witness objects provide their own verification methods
            if callable(getattr(H, 'is_sylow_p_subgroup', None)):
                return bool(H.is_sylow_p_subgroup(G, p))
            if hasattr(H, 'is_sylow_p_subgroup') and not callable(H.is_sylow_p_subgroup):
                return bool(H.is_sylow_p_subgroup)
            if callable(getattr(G, 'is_sylow_p_subgroup', None)):
                return bool(G.is_sylow_p_subgroup(H, p))
            if hasattr(H, 'is_sylow'):
                if callable(H.is_sylow):
                    return bool(H.is_sylow(G, p))
                return bool(H.is_sylow)
            
            # SymPy fallback for finite permutation groups
            if callable(getattr(H, 'is_subgroup', None)):
                if not H.is_subgroup(G):
                    return False
            else:
                return False
                
            h_order = H.order() if callable(getattr(H, 'order', None)) else H.order
            g_order = G.order() if callable(getattr(G, 'order', None)) else G.order
            
            if h_order == oo or g_order == oo or h_order == float('inf') or g_order == float('inf'):
                return False
                
            # Check if H is a p-group
            temp = h_order
            while temp % p == 0 and temp > 1:
                temp //= p
            if temp != 1:
                return False
                
            # Check if index of H in G is coprime to p (maximality condition for finite groups)
            index = g_order // h_order
            if index % p == 0:
                return False
                
            return True
        except Exception:
            return False

    try:
        h2 = check_sylow(P, G, p) and check_sylow(Q, G, p)
    except Exception:
        h2 = False

    # ¬Q: P is not isomorphic to Q
    try:
        if callable(getattr(P, 'is_isomorphic', None)):
            neg_q = not P.is_isomorphic(Q)
        elif callable(getattr(Q, 'is_isomorphic', None)):
            neg_q = not Q.is_isomorphic(P)
        elif callable(getattr(P, 'isomorphic', None)):
            neg_q = not P.isomorphic(Q)
        elif callable(getattr(Q, 'isomorphic', None)):
            neg_q = not Q.isomorphic(P)
        else:
            # SymPy fallback
            neg_q = not P.is_isomorphic(Q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P and Q are Sylow p-subgroups of G",
    "¬Q: P is not isomorphic to Q"
]

N_HYP = 2
NEG_Q_INDEX = 2