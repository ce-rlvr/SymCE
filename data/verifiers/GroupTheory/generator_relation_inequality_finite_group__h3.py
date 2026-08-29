import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
    try:
        # H1: G is a finite group
        if hasattr(witness, 'order'):
            ord_G = witness.order()
            h1_ok = (ord_G is not None) and (ord_G < float('inf'))
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    try:
        # H2: G has a finite presentation <X | R>
        if hasattr(witness, 'generators') and hasattr(witness, 'relators'):
            # Verify that generators and relators can be enumerated (finite)
            g_len = len(tuple(witness.generators))
            r_len = len(tuple(witness.relators))
            h2_ok = True
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    try:
        # ¬Q: The number of relations r is less than the number of generators g
        if hasattr(witness, 'generators') and hasattr(witness, 'relators'):
            g = len(tuple(witness.generators))
            r = len(tuple(witness.relators))
            neg_q_ok = bool(r < g)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G has a finite presentation <X | R>",
    "¬Q: The number of relations r is less than the number of generators g"
]

N_HYP = 2
NEG_Q_INDEX = 2