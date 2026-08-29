import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_semisimple(grp):
    """
    Helper function to determine if a group is semisimple.
    A group is semisimple if it has no non-trivial abelian normal subgroups.
    For our purposes, we check if it's abelian, solvable, or has a non-trivial center.
    """
    try:
        if not hasattr(grp, 'order'):
            return False
        if grp.order() == 1:
            return True
        if getattr(grp, 'is_abelian', False):
            return False
        if getattr(grp, 'is_solvable', False):
            return False
        if hasattr(grp, 'center') and grp.center().order() > 1:
            return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # H_1: H and K are groups such that G is isomorphic to the direct product H \times K
    h1_ok = False
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, H, K = witness
            elif len(witness) == 2:
                H, K = witness
                G = H * K
            else:
                G, H, K = None, None, None
        else:
            G, H, K = None, None, None
            
        if H is not None and K is not None and G is not None:
            if hasattr(H, 'generators') and hasattr(K, 'generators'):
                HK = H * K
                if hasattr(G, 'order') and G.order() == HK.order():
                    if G.is_isomorphic(HK):
                        h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: Both H and K are semisimple groups (must FAIL, so at least one is NOT semisimple)
    neg_q_ok = False
    try:
        if isinstance(witness, tuple) and len(witness) in (2, 3):
            if len(witness) == 3:
                _, H, K = witness
            else:
                H, K = witness
            
            H_semi = is_semisimple(H)
            K_semi = is_semisimple(K)
            neg_q_ok = not (H_semi and K_semi)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H and K are groups such that G is isomorphic to the direct product H \\times K",
    "¬Q: At least one of H or K is not a semisimple group"
]

N_HYP = 1
NEG_Q_INDEX = 1