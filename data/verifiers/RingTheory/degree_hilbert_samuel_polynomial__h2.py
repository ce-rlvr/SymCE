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

def _get_bool(w, keys):
    for k in keys:
        if isinstance(w, dict) and k in w:
            return bool(w[k])
        if hasattr(w, k):
            try:
                return bool(getattr(w, k))
            except Exception:
                pass
    return False

def _get_val(w, keys):
    for k in keys:
        if isinstance(w, dict) and k in w:
            return w[k]
        if hasattr(w, k):
            try:
                return getattr(w, k)
            except Exception:
                pass
    return None

def conditions(witness) -> list[bool]:
    try:
        h1 = _get_bool(witness, ['is_commutative', 'commutative']) and \
             _get_bool(witness, ['is_noetherian', 'noetherian']) and \
             _get_bool(witness, ['is_local', 'local'])
    except Exception:
        h1 = False

    try:
        h2 = _get_bool(witness, ['is_m_primary', 'm_primary', 'ideal_is_m_primary'])
    except Exception:
        h2 = False

    try:
        h3 = _get_bool(witness, ['is_hilbert_samuel_poly', 'is_HS_poly', 'is_hilbert_samuel'])
    except Exception:
        h3 = False

    try:
        deg_P = _get_val(witness, ['degree_P_I', 'deg_P', 'degree'])
        d = _get_val(witness, ['d', 'expected_d', 'krull_dimension', 'dim', 'dim_R'])
        if deg_P is not None and d is not None:
            neg_q = (deg_P != d)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (R, m) is a commutative Noetherian local ring",
    "H_2: I is an m-primary ideal of R",
    "H_3: P_I(n) is the Hilbert-Samuel polynomial associated to the I-adic filtration of R",
    "¬Q: The degree of the polynomial P_I(n) is not exactly d"
]

N_HYP = 3
NEG_Q_INDEX = 3