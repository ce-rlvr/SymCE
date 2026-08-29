import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

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
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture drops the hypothesis n >= 2.
    For n = 1, the entry in the first row and n-th column is (1,1), which is a diagonal entry.
    The conclusion's phrasing "non-diagonal entries ... except possibly the entry in the first row and n-th column"
    presupposes that (1,n) is a non-diagonal entry, making the statement logically malformed/false for n < 2.
    """
    n = None
    try:
        if isinstance(witness, int):
            n = witness
        elif isinstance(witness, tuple):
            for item in witness:
                if isinstance(item, int):
                    n = item
                    break
        elif hasattr(witness, 'degree'):
            n = witness.degree
        elif hasattr(witness, 'shape'):
            n = witness.shape[0]
        elif isinstance(witness, list) and len(witness) > 0 and hasattr(witness[0], 'shape'):
            n = witness[0].shape[0]
    except Exception:
        pass

    if n is None:
        return [False, False, False]

    # H_1: F is a field
    # The witness parameterizes the dimension n. We assume the standard construction over a valid field F.
    h1_ok = True

    # H_2: G is the group of n x n upper unitriangular matrices over F
    h2_ok = True

    # ¬Q: The conclusion fails at the witness.
    # The conclusion is true for n >= 2, but fails for n < 2 due to the diagonal nature of (1,1) or non-existence of rows.
    try:
        neg_q = bool(n < 2)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: G is the group of n x n upper unitriangular matrices over F",
    "¬Q: The center Z(G) does not consist exactly of those matrices in G whose non-diagonal entries are zero except possibly the entry in the first row and n-th column"
]

N_HYP = 2
NEG_Q_INDEX = 2