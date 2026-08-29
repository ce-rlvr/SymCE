import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    # The witness is expected to be a tuple of two groups: (G, H)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    def is_group(grp):
        return hasattr(grp, 'order') or hasattr(grp, 'generators') or hasattr(grp, 'elements')

    def is_profinite(grp):
        # In the context of discrete groups (which is what we represent computationally),
        # a group is profinite if and only if it is finite.
        try:
            if hasattr(grp, 'is_finite') and grp.is_finite is not None:
                return bool(grp.is_finite)
            if hasattr(grp, 'order'):
                ord_g = grp.order()
                return ord_g != sympy.oo
            if isinstance(grp, PermutationGroup):
                return True
        except Exception:
            pass
        return False

    # H_1: G is a profinite group
    try:
        h1_ok = bool(is_group(G) and is_profinite(G))
    except Exception:
        h1_ok = False

    # ¬Q: The direct product G x H is NOT a profinite group
    # G x H is profinite if and only if both G and H are profinite.
    try:
        if not (is_group(G) and is_group(H)):
            neg_q_ok = False
        else:
            g_prof = is_profinite(G)
            h_prof = is_profinite(H)
            neg_q_ok = not (g_prof and h_prof)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a profinite group",
    "¬Q: The direct product G x H is not a profinite group"
]

N_HYP = 1
NEG_Q_INDEX = 1