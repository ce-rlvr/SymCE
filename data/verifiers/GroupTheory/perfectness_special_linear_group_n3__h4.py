import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.domains import QQ, RR, CC, ZZ
from sympy import GF, S
from sympy.polys.domains.field import Field

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
O2 = zeros(2,2)
O3 = zeros(3,3)

Q = QQ
R = RR
C = CC
F2 = GF(2)
F3 = GF(3)
F5 = GF(5)

def conditions(witness) -> list[bool]:
    n, F, G = None, None, None
    if isinstance(witness, dict):
        n = witness.get('n')
        F = witness.get('F')
        G = witness.get('G')
    elif isinstance(witness, (list, tuple)) and len(witness) == 3:
        n, F, G = witness

    # H_1: n is an integer
    try:
        h1 = isinstance(n, int) or (hasattr(n, 'is_integer') and n.is_integer)
    except Exception:
        h1 = False

    # H_2: n >= 3
    try:
        h2 = int(n) >= 3
    except Exception:
        h2 = False

    # H_3: F is a field
    try:
        if isinstance(F, Field):
            h3 = True
        elif F in [S.Reals, S.Complexes, S.Rationals]:
            h3 = True
        elif isinstance(F, str) and F.upper() in ['Q', 'R', 'C', 'F2', 'F3', 'F5', 'FIELD']:
            h3 = True
        elif hasattr(F, 'is_Field') and F.is_Field:
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The commutator subgroup of G is not equal to G
    try:
        if hasattr(G, 'derived_subgroup'):
            derived = G.derived_subgroup()
            neg_q = derived.order() != G.order()
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "H_2: n >= 3",
    "H_3: F is a field",
    "¬Q: The commutator subgroup of G is not equal to G"
]

N_HYP = 3
NEG_Q_INDEX = 3