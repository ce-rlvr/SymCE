import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    G = None
    n = None
    f = None
    
    try:
        if isinstance(witness, tuple):
            G = witness[0]
            if len(witness) > 1:
                n = witness[1]
            if len(witness) > 2:
                f = witness[2]
        else:
            G = witness
    except Exception:
        pass

    # H_1: G is an abelian group
    try:
        h1 = bool(G.is_abelian)
    except Exception:
        h1 = False

    # H_2: n is an integer
    try:
        h2 = isinstance(n, (int, sympy.Integer))
    except Exception:
        h2 = False

    # ¬Q: f is not a group homomorphism
    try:
        if f is None:
            f_map = lambda x: x**n
        elif isinstance(f, dict):
            f_map = lambda x: f[x]
        else:
            f_map = f

        is_hom = True
        elements = list(G.elements)
        for x in elements:
            for y in elements:
                if f_map(x * y) != f_map(x) * f_map(y):
                    is_hom = False
                    break
            if not is_hom:
                break
        neg_q = not is_hom
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: n is an integer",
    "¬Q: f is not a group homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2