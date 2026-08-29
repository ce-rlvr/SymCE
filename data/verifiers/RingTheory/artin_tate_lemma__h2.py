import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_bool(w, *keys):
    """Helper to extract boolean properties from a dictionary or object witness."""
    if isinstance(w, dict):
        for k in keys:
            if k in w:
                return bool(w[k])
    else:
        for k in keys:
            if hasattr(w, k):
                return bool(getattr(w, k))
            elif hasattr(w, '__getitem__'):
                try:
                    return bool(w[k])
                except (KeyError, TypeError):
                    pass
    return False

def conditions(witness) -> list[bool]:
    try:
        # H1: R, S, and T are commutative rings such that R <= S <= T
        h1_comm = get_bool(witness, 'commutative_rings', 'are_commutative_rings') or \
                  (get_bool(witness, 'R_is_commutative_ring', 'R_commutative', 'R_is_commutative') and
                   get_bool(witness, 'S_is_commutative_ring', 'S_commutative', 'S_is_commutative') and
                   get_bool(witness, 'T_is_commutative_ring', 'T_commutative', 'T_is_commutative'))
        
        h1_sub = get_bool(witness, 'R_subset_S_subset_T', 'chain_condition') or \
                 (get_bool(witness, 'R_subset_S', 'R_in_S', 'R_subseteq_S', 'R_sub_S') and
                  get_bool(witness, 'S_subset_T', 'S_in_T', 'S_subseteq_T', 'S_sub_T'))
                  
        h1 = h1_comm and h1_sub
    except Exception:
        h1 = False

    try:
        # H2: T is finitely generated as an algebra over R
        h2 = get_bool(witness, 'T_is_fg_R_algebra', 'T_fg_R_algebra', 'T_finitely_generated_R_algebra', 'T_fg_over_R')
    except Exception:
        h2 = False

    try:
        # H3: T is finitely generated as a module over S
        h3 = get_bool(witness, 'T_is_fg_S_module', 'T_fg_S_module', 'T_finitely_generated_S_module', 'T_fg_module_over_S')
    except Exception:
        h3 = False

    try:
        # neg_Q: S is NOT finitely generated as an algebra over R
        # (The conclusion is that S IS finitely generated, so we negate it)
        neg_q = not get_bool(witness, 'S_is_fg_R_algebra', 'S_fg_R_algebra', 'S_finitely_generated_R_algebra', 'S_fg_over_R')
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R, S, and T are commutative rings such that R <= S <= T",
    "H_2: T is finitely generated as an algebra over R",
    "H_3: T is finitely generated as a module over S",
    "¬Q: S is not finitely generated as an algebra over R"
]

N_HYP = 3
NEG_Q_INDEX = 3