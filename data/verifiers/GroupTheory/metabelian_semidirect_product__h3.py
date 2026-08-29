import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict) and 'G' in witness:
            G = witness['G']
            N = witness.get('N', trivial)
            H = witness.get('H', trivial)
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, N, H = witness
        elif hasattr(witness, 'G'):
            G = witness.G
            N = getattr(witness, 'N', trivial)
            H = getattr(witness, 'H', trivial)
        else:
            G = witness
            N = trivial
            H = trivial
    except Exception:
        return [False, False, False]

    # H_1: N is an abelian group
    try:
        h1 = bool(N.is_abelian)
    except Exception:
        h1 = False

    # H_2: H is an abelian group
    try:
        h2 = bool(H.is_abelian)
    except Exception:
        h2 = False

    # ¬Q: G is not a metabelian group
    try:
        derived = G.derived_subgroup()
        is_metabelian = bool(derived.is_abelian)
        neg_q = not is_metabelian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is an abelian group",
    "H_2: H is an abelian group",
    "¬Q: G is not a metabelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2