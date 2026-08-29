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

from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The conjecture is true for commutative rings, so the counterexample must be
    a non-commutative ring ideal (or a mock object representing one).
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_proper_ideal', False))
            h2 = bool(witness.get('is_finite_intersection_of_primary', witness.get('has_primary_decomposition', False)))
            q = bool(witness.get('has_irredundant_primary_decomposition_with_distinct_radicals', witness.get('has_distinct_radicals_decomposition', True)))
            neg_q = not q
        elif isinstance(witness, (tuple, list)) and len(witness) >= 3 and all(isinstance(x, bool) for x in witness[:3]):
            h1 = bool(witness[0])
            h2 = bool(witness[1])
            neg_q = not bool(witness[2])
        else:
            h1_attr = getattr(witness, 'is_proper_ideal', False)
            h1 = bool(h1_attr() if callable(h1_attr) else h1_attr)
            
            h2_attr = getattr(witness, 'is_finite_intersection_of_primary', getattr(witness, 'has_primary_decomposition', False))
            h2 = bool(h2_attr() if callable(h2_attr) else h2_attr)
            
            q_attr = getattr(witness, 'has_irredundant_primary_decomposition_with_distinct_radicals', getattr(witness, 'has_distinct_radicals_decomposition', True))
            q = bool(q_attr() if callable(q_attr) else q_attr)
            neg_q = not q
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "H_2: I can be expressed as a finite intersection of primary ideals",
    "¬Q: I cannot be expressed as an irredundant finite intersection of primary ideals where the radicals of the primary components are distinct"
]

N_HYP = 2
NEG_Q_INDEX = 2