import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: G has a solvable conjugacy problem",
    "H_3: H has a solvable conjugacy problem",
    "¬Q: The direct product G × H does not have a solvable conjugacy problem"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # Handle dictionary-based mock witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('G_is_finitely_generated', False))
            h2 = bool(witness.get('G_has_solvable_conjugacy_problem', False))
            h3 = bool(witness.get('H_has_solvable_conjugacy_problem', False))
            neg_q = not bool(witness.get('GxH_has_solvable_conjugacy_problem', True))
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # Handle object-based mock witness with attributes
    if hasattr(witness, 'G_is_finitely_generated'):
        try:
            h1 = bool(getattr(witness, 'G_is_finitely_generated', False))
            h2 = bool(getattr(witness, 'G_has_solvable_conjugacy_problem', False))
            h3 = bool(getattr(witness, 'H_has_solvable_conjugacy_problem', False))
            neg_q = not bool(getattr(witness, 'GxH_has_solvable_conjugacy_problem', True))
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # Handle tuple witness (G, H)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def is_fg(g):
        if hasattr(g, 'is_finitely_generated'):
            val = g.is_finitely_generated
            return bool(val() if callable(val) else val)
        # Standard SymPy permutation groups are finite, hence finitely generated
        return True

    def has_scp(g):
        if hasattr(g, 'has_solvable_conjugacy_problem'):
            val = g.has_solvable_conjugacy_problem
            return bool(val() if callable(val) else val)
        # Standard SymPy permutation groups are finite, hence have solvable conjugacy problem
        return True

    try:
        h1 = is_fg(G)
    except Exception:
        h1 = False

    try:
        h2 = has_scp(G)
    except Exception:
        h2 = False

    try:
        h3 = has_scp(H)
    except Exception:
        h3 = False

    try:
        # The conjugacy problem for G x H is solvable if and only if it is solvable for both G and H,
        # AND G x H is finitely generated (which requires both G and H to be finitely generated).
        gxh_scp = has_scp(G) and has_scp(H) and is_fg(G) and is_fg(H)
        neg_q = not gxh_scp
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]