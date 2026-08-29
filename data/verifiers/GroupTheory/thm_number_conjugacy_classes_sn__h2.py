import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import npartitions

# Top-level setup: named object bindings that the witness expression may reference
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks whether it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (G, n) where G is a group and n is an integer,
    demonstrating the scope extrusion of the variable n between the hypothesis and conclusion.
    """
    # Unpack witness
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            if hasattr(witness[0], 'conjugacy_classes'):
                G, n = witness
            elif hasattr(witness[1], 'conjugacy_classes'):
                n, G = witness
            else:
                G, n = witness
        else:
            G = witness
            n = getattr(G, 'degree', None)
    except Exception:
        return [False, False]

    # H_1: G is the symmetric group S_k for some positive integer k
    try:
        h1 = False
        if hasattr(G, 'is_symmetric') and hasattr(G, 'conjugacy_classes'):
            if callable(G.is_symmetric):
                h1 = bool(G.is_symmetric())
            else:
                h1 = bool(G.is_symmetric)
    except Exception:
        h1 = False

    # ¬Q: The number of distinct conjugacy classes of G is NOT exactly p(n)
    try:
        n_val = int(n)
        if n_val <= 0:
            neg_q = False
        else:
            num_classes = len(G.conjugacy_classes())
            p_n = npartitions(n_val)
            neg_q = bool(num_classes != p_n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the symmetric group S_n for some positive integer n",
    "¬Q: The number of distinct conjugacy classes of G is not exactly p(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1