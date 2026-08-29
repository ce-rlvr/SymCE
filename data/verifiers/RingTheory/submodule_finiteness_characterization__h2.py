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

# Top-level setup
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

def get_bool_prop(obj, prop_names, default=False):
    if isinstance(obj, dict):
        for name in prop_names:
            if name in obj:
                return bool(obj[name])
    for name in prop_names:
        if hasattr(obj, name):
            val = getattr(obj, name)
            if callable(val):
                try:
                    return bool(val())
                except Exception:
                    pass
            else:
                return bool(val)
    return default

def conditions(witness) -> list[bool]:
    # The witness may be a single object/dict containing properties for both R and M,
    # or a tuple (R, M), or an object with .R and .M attributes.
    R = witness
    M = witness
    if isinstance(witness, tuple) and len(witness) == 2:
        R, M = witness
    elif hasattr(witness, 'R') and hasattr(witness, 'M'):
        R = witness.R
        M = witness.M

    try:
        h1 = get_bool_prop(R, ['is_ring', 'is_Ring', 'is_ring_obj'], default=False)
    except Exception:
        h1 = False

    try:
        is_noeth = get_bool_prop(M, ['is_noetherian_module', 'is_noetherian', 'is_Noetherian'], default=False)
        every_fg = get_bool_prop(M, ['every_submodule_finitely_generated', 'all_submodules_finitely_generated', 'submodules_finitely_generated'], default=False)
        
        # The conclusion Q is: M is a Noetherian module iff every submodule of M is finitely generated.
        # Therefore, Q is True if is_noeth == every_fg.
        # The negated conclusion neg_Q is True if Q is False, i.e., is_noeth != every_fg.
        neg_q = (is_noeth != every_fg)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: M is a Noetherian module is not equivalent to every submodule of M being finitely generated"
]

N_HYP = 1
NEG_Q_INDEX = 1