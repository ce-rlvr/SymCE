import sympy
from sympy.combinatorics import PermutationGroup
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
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The quotient group G/Z(G) is nilpotent
    try:
        if not h1:
            h2 = False
        else:
            Z = witness.center
            if callable(Z):
                Z = Z()
            lcs = witness.lower_central_series
            if callable(lcs):
                lcs = lcs()
            gens = lcs[-1].generators
            if callable(gens):
                gens = gens()
            h2 = all(g in Z for g in gens)
    except Exception:
        h2 = False

    # ¬Q: G is not a nilpotent group
    try:
        if not h1:
            neg_q = False
        else:
            nilp = witness.is_nilpotent
            if callable(nilp):
                nilp = nilp()
            neg_q = not bool(nilp)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The quotient group G/Z(G) is nilpotent",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 2
NEG_Q_INDEX = 2