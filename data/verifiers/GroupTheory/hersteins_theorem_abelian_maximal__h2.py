import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
trivial = PermutationGroup([Permutation(0)])
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            M = witness.get('M')
        elif hasattr(witness, 'G') and hasattr(witness, 'M'):
            G = witness.G
            M = witness.M
        else:
            G, M = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(M, PermutationGroup) and M.is_subgroup(G)
    except Exception:
        h1_ok = False

    try:
        h2_ok = (M.is_abelian == True)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = (G.is_solvable == False)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group and M is a subgroup of G",
    "H_2: M is an abelian group",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2