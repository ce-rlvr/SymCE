import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: E/F is a finite Galois extension",
    "H_2: Gal(E/F) is a cyclic group of order n",
    "¬Q: There does not exist a unique intermediate field K such that the degree of K over F is exactly d"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, d = witness
        elif isinstance(witness, dict) and 'n' in witness and 'd' in witness:
            G = witness['n']
            d = witness['d']
        elif isinstance(witness, dict) and 'G' in witness and 'd' in witness:
            G = witness['G']
            d = witness['d']
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        if type(G) is int:
            h1 = (G >= 1) and type(d) is int and (d >= 1)
        else:
            h1 = (hasattr(G, 'is_group') or hasattr(G, 'order')) and type(d) is int and (d >= 1)
    except Exception:
        h1 = False

    try:
        if type(G) is int:
            h2 = True
            n = G
        else:
            h2 = bool(G.is_cyclic)
            n = G.order()
    except Exception:
        h2 = False
        n = 1

    try:
        neg_q = (n % d != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]