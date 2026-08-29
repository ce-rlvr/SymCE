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

# Top-level setup: named object bindings
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

def _get_prop(witness, prop_names):
    """Helper to extract properties from a dictionary or object witness."""
    if isinstance(witness, dict):
        for name in prop_names:
            if name in witness:
                val = witness[name]
                return val() if callable(val) else val
    else:
        for name in prop_names:
            if hasattr(witness, name):
                val = getattr(witness, name)
                return val() if callable(val) else val
    raise AttributeError(f"Missing property: {prop_names[0]}")

def conditions(witness) -> list[bool]:
    # If the witness is provided directly as a list/tuple of 4 booleans
    if isinstance(witness, (list, tuple)) and len(witness) == 4:
        try:
            return [bool(witness[0]), bool(witness[1]), bool(witness[2]), bool(witness[3])]
        except Exception:
            return [False, False, False, False]

    # H1: R is a commutative Noetherian ring
    try:
        h1 = bool(_get_prop(witness, ['R_is_commutative_Noetherian', 'is_commutative_Noetherian', 'h1']))
    except Exception:
        h1 = False

    # H2: I is an ideal of R
    try:
        h2 = bool(_get_prop(witness, ['I_is_ideal', 'is_ideal', 'h2']))
    except Exception:
        h2 = False

    # H3: N is the intersection of I^n M for all positive integers n
    try:
        h3 = bool(_get_prop(witness, ['N_is_intersection', 'is_intersection', 'h3']))
    except Exception:
        h3 = False

    # ¬Q: IN != N (The conclusion IN = N must FAIL)
    try:
        try:
            in_equals_n = bool(_get_prop(witness, ['IN_equals_N', 'in_equals_n', 'q']))
            neg_q = not in_equals_n
        except AttributeError:
            neg_q = bool(_get_prop(witness, ['IN_not_equals_N', 'in_not_equals_n', 'neg_q']))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: I is an ideal of R",
    "H_3: N is the intersection of I^n M for all positive integers n",
    "¬Q: IN != N"
]

N_HYP = 3
NEG_Q_INDEX = 3