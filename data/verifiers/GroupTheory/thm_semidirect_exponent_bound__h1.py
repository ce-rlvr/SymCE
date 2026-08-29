import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup
from sympy import lcm

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

def group_exponent(grp):
    """Helper to compute the exponent of a finite group."""
    try:
        # Prevent hanging on very large groups
        if hasattr(grp, 'order'):
            if callable(grp.order):
                if grp.order() > 10000:
                    return None
            else:
                if grp.order > 10000:
                    return None
    except Exception:
        pass
        
    e = 1
    try:
        for g in grp.elements:
            e = lcm(e, g.order())
        return int(e)
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    # Extract G, N, H from the witness
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, N, H = witness
        elif hasattr(witness, 'G') and hasattr(witness, 'N') and hasattr(witness, 'H'):
            G = witness.G
            N = witness.N
            H = witness.H
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: N has finite exponent e_N
    try:
        e_N = group_exponent(N)
        h1 = (e_N is not None) and (e_N > 0)
    except Exception:
        h1 = False

    # H_2: H has finite exponent e_H
    try:
        e_H = group_exponent(H)
        h2 = (e_H is not None) and (e_H > 0)
    except Exception:
        h2 = False

    # ¬Q: The exponent of G is NOT finite OR does NOT divide the integer product e_N e_H.
    try:
        e_G = group_exponent(G)
        if e_G is None or e_G <= 0:
            # If we cannot compute a finite exponent, we conservatively return False 
            # to avoid false positives on invalid objects.
            neg_q = False
        else:
            if not h1 or not h2:
                neg_q = False
            else:
                neg_q = ((e_N * e_H) % e_G != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N has finite exponent e_N",
    "H_2: H has finite exponent e_H",
    "¬Q: The exponent of G does not divide e_N * e_H"
]

N_HYP = 2
NEG_Q_INDEX = 2