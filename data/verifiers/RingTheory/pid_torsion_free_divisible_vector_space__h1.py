import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import *
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample to the conjecture.
    The witness is expected to be a dictionary or an object with attributes corresponding
    to the hypotheses and the conclusion.
    """
    def extract(names, default=False):
        if isinstance(witness, dict):
            for name in names:
                if name in witness:
                    val = witness[name]
                    return bool(val() if callable(val) else val)
        for name in names:
            if hasattr(witness, name):
                val = getattr(witness, name)
                return bool(val() if callable(val) else val)
        return default

    # H_1: K is the field of fractions of R
    try:
        h1 = extract(['K_is_field_of_fractions_of_R', 'is_field_of_fractions', 'h1'])
    except Exception:
        h1 = False

    # H_2: M is an R-module
    try:
        h2 = extract(['M_is_R_module', 'is_R_module', 'h2'])
    except Exception:
        h2 = False

    # H_3: M is torsion-free
    try:
        h3 = extract(['M_is_torsion_free', 'is_torsion_free', 'h3'])
    except Exception:
        h3 = False

    # H_4: M is divisible
    try:
        h4 = extract(['M_is_divisible', 'is_divisible', 'h4'])
    except Exception:
        h4 = False

    # ¬Q: M does NOT admit a unique K-vector space structure extending its R-module structure
    try:
        if isinstance(witness, dict) and any(k in witness for k in ['neg_q', 'not_admits_unique_K_vector_space_structure']):
            neg_q = extract(['neg_q', 'not_admits_unique_K_vector_space_structure'])
        elif any(hasattr(witness, k) for k in ['neg_q', 'not_admits_unique_K_vector_space_structure']):
            neg_q = extract(['neg_q', 'not_admits_unique_K_vector_space_structure'])
        else:
            q = extract(['admits_unique_K_vector_space_structure', 'admits_unique_structure', 'q'], default=True)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "H_2: M is an R-module",
    "H_3: M is torsion-free",
    "H_4: M is divisible",
    "¬Q: M does not admit a unique K-vector space structure extending its R-module structure"
]

N_HYP = 4
NEG_Q_INDEX = 4