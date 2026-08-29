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

def conditions(witness) -> list[bool]:
    # H_1: N is the nilradical of R
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_nilradical', witness.get('N_is_nilradical', witness.get('N_is_nilradical_of_R', False))))
        else:
            h1 = bool(getattr(witness, 'is_nilradical', getattr(witness, 'N_is_nilradical', getattr(witness, 'N_is_nilradical_of_R', False))))
    except Exception:
        h1 = False

    # ¬Q: The Krull dimension of R is not equal to the Krull dimension of R/N
    try:
        if isinstance(witness, dict):
            dim_R = witness.get('dim_R', witness.get('krull_dim_R', witness.get('krull_dimension_R')))
            dim_R_mod_N = witness.get('dim_R_mod_N', witness.get('krull_dim_R_mod_N', witness.get('krull_dimension_R_mod_N')))
        else:
            dim_R = getattr(witness, 'dim_R', getattr(witness, 'krull_dim_R', getattr(witness, 'krull_dimension_R', None)))
            dim_R_mod_N = getattr(witness, 'dim_R_mod_N', getattr(witness, 'krull_dim_R_mod_N', getattr(witness, 'krull_dimension_R_mod_N', None)))
            
        if dim_R is not None and dim_R_mod_N is not None:
            neg_q = (dim_R != dim_R_mod_N)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is the nilradical of R",
    "¬Q: The Krull dimension of R is not equal to the Krull dimension of R/N"
]

N_HYP = 1
NEG_Q_INDEX = 1