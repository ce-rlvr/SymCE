import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def _is_fc_group(g):
    type_str = str(type(g))
    if 'FreeGroup' in type_str:
        return len(g.generators) <= 1
    if hasattr(g, 'is_abelian') and g.is_abelian:
        return True
    if hasattr(g, 'is_finite') and g.is_finite:
        return True
    if 'PermutationGroup' in type_str or 'NamedGroup' in type_str:
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = bool(_is_fc_group(G))
    except Exception:
        h1_ok = False

    try:
        q_ok = _is_fc_group(G) and _is_fc_group(H)
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is an FC-group",
    "¬Q: The direct product G x H is not an FC-group"
]

N_HYP = 1
NEG_Q_INDEX = 1