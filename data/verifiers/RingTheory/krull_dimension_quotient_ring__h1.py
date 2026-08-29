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
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.DihedralGroup(2)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def get_is_proper(witness):
    for attr in ['is_proper_ideal', 'is_proper', 'proper_ideal']:
        if hasattr(witness, attr):
            val = getattr(witness, attr)
            val = val() if callable(val) else val
            if isinstance(val, str):
                return val.lower() == 'true'
            return val
    if isinstance(witness, dict):
        for key in ['is_proper_ideal', 'is_proper', 'proper_ideal']:
            if key in witness:
                val = witness[key]
                if isinstance(val, str):
                    return val.lower() == 'true'
                return val
    if isinstance(witness, tuple) and len(witness) >= 3:
        for item in witness:
            if isinstance(item, bool):
                return item
    return False

def get_dim_R(witness):
    for attr in ['dim_R', 'krull_dim_R', 'krull_dimension_R', 'dim']:
        if hasattr(witness, attr):
            val = getattr(witness, attr)
            val = val() if callable(val) else val
            try:
                return float(val)
            except Exception:
                pass
    if isinstance(witness, dict):
        for key in ['dim_R', 'krull_dim_R', 'krull_dimension_R', 'dim']:
            if key in witness:
                try:
                    return float(witness[key])
                except Exception:
                    pass
    if isinstance(witness, tuple) and len(witness) >= 3:
        nums = [x for x in witness if isinstance(x, (int, float)) and not isinstance(x, bool)]
        if len(nums) >= 2:
            return float(nums[0])
    return None

def get_dim_R_mod_I(witness):
    for attr in ['dim_R_mod_I', 'krull_dim_R_mod_I', 'krull_dimension_R_mod_I', 'dim_mod', 'dim_quotient']:
        if hasattr(witness, attr):
            val = getattr(witness, attr)
            val = val() if callable(val) else val
            try:
                return float(val)
            except Exception:
                pass
    if isinstance(witness, dict):
        for key in ['dim_R_mod_I', 'krull_dim_R_mod_I', 'krull_dimension_R_mod_I', 'dim_mod', 'dim_quotient']:
            if key in witness:
                try:
                    return float(witness[key])
                except Exception:
                    pass
    if isinstance(witness, tuple) and len(witness) >= 3:
        nums = [x for x in witness if isinstance(x, (int, float)) and not isinstance(x, bool)]
        if len(nums) >= 2:
            return float(nums[1])
    return None

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(get_is_proper(witness))
    except Exception:
        h1 = False

    try:
        dim_R = get_dim_R(witness)
        dim_R_mod_I = get_dim_R_mod_I(witness)
        if dim_R is not None and dim_R_mod_I is not None:
            neg_q = dim_R_mod_I > dim_R
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: The Krull dimension of the quotient ring R/I is strictly greater than the Krull dimension of R"
]

N_HYP = 1
NEG_Q_INDEX = 1