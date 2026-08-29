import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    try:
        F, x, y = witness
    except Exception:
        return [False, False, False]

    # H1: x and y are elements of F
    try:
        if hasattr(F, 'contains'):
            h1 = bool(F.contains(x) and F.contains(y))
        else:
            elements = list(F.elements) if hasattr(F, 'elements') else list(F)
            h1 = bool(x in elements and y in elements)
    except Exception:
        h1 = False

    # H2: xy = yx
    try:
        h2 = bool(x * y == y * x)
    except Exception:
        h2 = False

    # ¬Q: There is NO z in F such that x = z^p and y = z^q
    try:
        if hasattr(F, 'elements'):
            elements = list(F.elements)
        else:
            elements = list(F)
            
        def get_powers(z):
            p = [z]
            curr = z
            for _ in range(10000):
                curr = curr * z
                if curr == z:
                    break
                p.append(curr)
            return p

        neg_q = True
        for z in elements:
            powers = get_powers(z)
            if x in powers and y in powers:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of F",
    "H_2: xy = yx",
    "¬Q: There is no z in F such that x and y are powers of z"
]

N_HYP = 2
NEG_Q_INDEX = 2