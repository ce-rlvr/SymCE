import sympy
from sympy.combinatorics import PermutationGroup, DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import is_perfect as is_perfect_num

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)  # Smallest perfect group
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: (G x H is perfect) is not equivalent to (both G and H are perfect)"
]

def is_perfect_obj(obj):
    """
    Checks if an object is 'perfect'.
    For groups, it means the derived subgroup equals the group itself.
    For numbers, it means it is a perfect number (e.g., 6, 28).
    """
    if isinstance(obj, PermutationGroup):
        try:
            return obj.derived_subgroup().order() == obj.order()
        except Exception:
            return False
    try:
        if is_perfect_num(obj):
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # Extract G and H from the witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            G = getattr(witness, 'G', None)
            H = getattr(witness, 'H', None)
            
        if G is None or H is None:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # neg_Q: The direct product G x H is perfect if and only if both G and H are perfect.
    # We evaluate the conclusion and return its negation.
    try:
        g_perf = is_perfect_obj(G)
        h_perf = is_perfect_obj(H)
        both_perf = bool(g_perf and h_perf)

        try:
            GxH = DirectProduct(G, H)
            gxh_perf = GxH.derived_subgroup().order() == GxH.order()
        except Exception:
            # If DirectProduct fails (e.g., H is not a group), G x H is not a perfect group
            gxh_perf = False

        # The conclusion is that gxh_perf == both_perf
        # We want the negation of the conclusion
        neg_q_ok = (gxh_perf != both_perf)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]