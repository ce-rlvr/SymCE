import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    # If the witness is provided as a tuple (k, E) or (k, E, gens), 
    # we extract E if it appears to be the algebraic structure.
    if isinstance(witness, tuple) and len(witness) >= 2:
        if hasattr(witness[1], "is_field") or hasattr(witness[1], "is_Field") or isinstance(witness[1], dict):
            witness = witness[1]

    # Handle dictionary-based witness
    if isinstance(witness, dict):
        h1 = bool(witness.get("is_finitely_generated_k_algebra", False))
        h2 = bool(witness.get("is_field", False))
        neg_q = not bool(witness.get("is_finite_algebraic_extension", True))
        return [h1, h2, neg_q]

    # Handle object-based witness via duck-typing
    try:
        if hasattr(witness, "is_finitely_generated_k_algebra"):
            val = witness.is_finitely_generated_k_algebra
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, "is_finitely_generated_algebra"):
            val = witness.is_finitely_generated_algebra
            h1 = bool(val() if callable(val) else val)
    except Exception:
        pass

    try:
        if hasattr(witness, "is_field"):
            val = witness.is_field
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, "is_Field"):
            val = witness.is_Field
            h2 = bool(val() if callable(val) else val)
    except Exception:
        pass

    try:
        if hasattr(witness, "is_finite_algebraic_extension"):
            val = witness.is_finite_algebraic_extension
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, "is_finite_extension"):
            val = witness.is_finite_extension
            neg_q = not bool(val() if callable(val) else val)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is a finitely generated k-algebra",
    "H_2: E is a field",
    "¬Q: E is not a finite algebraic extension of k"
]

N_HYP = 2
NEG_Q_INDEX = 2