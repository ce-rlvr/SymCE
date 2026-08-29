import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings for the witness expression
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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two groups (G, H).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    try:
        # A group is left-orderable if it admits a strict total order invariant under left multiplication.
        # For finite groups, only the trivial group (order 1) is left-orderable, 
        # because any non-identity element would generate torsion, violating left-orderability.
        h1 = (G.order() == 1)
    except Exception:
        h1 = False

    try:
        # The direct product G x H of finite groups is left-orderable if and only if 
        # it is the trivial group (i.e., its order is 1).
        # The conclusion FAILS (neg_Q is True) if G x H is NOT left-orderable,
        # which means its order is strictly greater than 1.
        neg_q = (G.order() * H.order() > 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a left-orderable group",
    "¬Q: The direct product G x H is not a left-orderable group"
]

N_HYP = 1
NEG_Q_INDEX = 1