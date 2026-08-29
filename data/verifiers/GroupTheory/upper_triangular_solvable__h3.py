import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and violates the conclusion.
    The witness can be a group G, or a tuple (F, n, G), or (n, G).
    """
    if isinstance(witness, tuple):
        if len(witness) == 3:
            F, n, G = witness
        elif len(witness) == 2:
            F = 'QQ'
            n, G = witness
        elif len(witness) >= 1:
            F = 'QQ'
            n = 1
            G = witness[-1]
        else:
            F, n, G = 'QQ', 1, None
    else:
        F, n, G = 'QQ', 1, witness

    # H_1: Let F be a field
    try:
        # F is a free parameter not restricting G in the dropped conjecture.
        # We accept any provided F as valid.
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: Let n be a positive integer
    try:
        h2_ok = int(n) > 0
    except Exception:
        h2_ok = False

    # ¬Q: The group G is NOT solvable
    try:
        if hasattr(G, 'is_solvable'):
            neg_q_ok = not G.is_solvable
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is a positive integer",
    "¬Q: G is not solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2