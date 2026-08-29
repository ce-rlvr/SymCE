import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    try:
        if isinstance(witness, dict):
            h1 = witness.get('has_zero_ideal', False) or witness.get('zero_ideal') in ({0}, [0], 0, '{0}')
        else:
            h1 = getattr(witness, 'has_zero_ideal', False) or getattr(witness, 'zero_ideal', None) in ({0}, [0], 0, '{0}')
    except Exception:
        h1 = False

    neg_q = False
    try:
        if isinstance(witness, dict):
            neg_q = not witness.get('is_isomorphic', True)
        else:
            zero_ideal = getattr(witness, 'zero_ideal', {0})
            q_ring = witness.quotient_ring(zero_ideal)
            if hasattr(q_ring, 'is_isomorphic'):
                neg_q = not q_ring.is_isomorphic(witness)
            elif hasattr(witness, 'is_isomorphic'):
                neg_q = not witness.is_isomorphic(q_ring)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: {0} is the zero ideal of R",
    "¬Q: The quotient ring R/{0} is not isomorphic to R"
]

N_HYP = 1
NEG_Q_INDEX = 1