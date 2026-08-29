import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    # The witness is expected to be a tuple (G, M)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, M = witness
        else:
            G = witness.G
            M = witness.M
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        # In SymPy, PermutationGroup instances are finite groups.
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: M is a nilpotent group
    try:
        h2_ok = isinstance(M, PermutationGroup) and bool(M.is_nilpotent)
    except Exception:
        h2_ok = False

    # H_3: The order of M is an odd integer
    try:
        try:
            order = M.order()
        except TypeError:
            order = M.order
        h3_ok = (order % 2 == 1)
    except Exception:
        h3_ok = False

    # ¬Q: G is not a solvable group
    try:
        neg_q_ok = not bool(G.is_solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: M is a nilpotent group",
    "H_3: The order of M is an odd integer",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3