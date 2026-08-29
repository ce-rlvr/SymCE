import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
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
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since the counterexample must be an infinite non-commutative ring 
    (e.g., upper triangular matrices over Q and Q[x]_{(x)}), which cannot be 
    natively represented and evaluated in SymPy, the witness is expected to 
    provide its properties either via an object interface or a dictionary.
    """
    # Attempt 1: Object with R, I, J attributes and methods
    try:
        R = witness.R
        I = witness.I
        J = witness.J
        
        h1 = bool(I.is_finitely_generated_ideal(R))
        h2 = bool(J.is_ideal(R))
        h3 = bool(J.is_contained_in_jacobson_radical(R))
        h4 = bool(I == I * J)
        neg_q = bool(I != R.zero_ideal())
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # Attempt 2: Dictionary format
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('I_is_finitely_generated_ideal', False))
            h2 = bool(witness.get('J_is_ideal', False))
            h3 = bool(witness.get('J_in_jacobson_radical', False))
            h4 = bool(witness.get('I_equals_IJ', False))
            neg_q = not bool(witness.get('I_is_zero', True))
            return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # Attempt 3: Simple boolean attributes on the witness object
    try:
        h1 = bool(witness.I_is_finitely_generated_ideal)
        h2 = bool(witness.J_is_ideal)
        h3 = bool(witness.J_in_jacobson_radical)
        h4 = bool(witness.I_equals_IJ)
        neg_q = not bool(witness.I_is_zero)
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: I is a finitely generated ideal of R",
    "H_2: J is an ideal of R",
    "H_3: J is contained in the Jacobson radical of R",
    "H_4: I = IJ",
    "¬Q: I is not {0}"
]

N_HYP = 4
NEG_Q_INDEX = 4