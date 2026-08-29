import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        if isinstance(witness, dict):
            G = witness['G']
            c = int(witness['c'])
            x = witness['x']
            y = witness['y']
        else:
            if len(witness) == 4:
                G, c, x, y = witness
                c = int(c)
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(G.contains(x))
    except Exception:
        h1 = False

    try:
        h2 = bool(G.contains(y))
    except Exception:
        h2 = False

    try:
        def get_inv(g):
            try:
                return ~g
            except Exception:
                return g**(-1)

        res = x
        for _ in range(c):
            res = get_inv(res) * get_inv(y) * res * y
        
        try:
            is_id = bool(res.is_Identity)
        except Exception:
            try:
                is_id = bool(res == G.identity)
            except Exception:
                is_id = False
                
        neg_q = not is_id
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "H_2: y is an element of G",
    "¬Q: The c-fold left-normed commutator is not equal to the identity element of G"
]

N_HYP = 2
NEG_Q_INDEX = 2