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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since SymPy does not have a native representation for abstract R-modules and 
    Artinian properties, this verifier expects the witness to be a dictionary, 
    a tuple of booleans, or an object with the relevant boolean attributes.
    """
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_short_exact_sequence', False))
            h2 = bool(witness.get('M_prime_is_artinian', False))
            h3 = bool(witness.get('M_double_prime_is_artinian', False))
            neg_q = not bool(witness.get('M_is_artinian', True))
        elif isinstance(witness, (list, tuple)) and len(witness) >= 4:
            h1 = bool(witness[0])
            h2 = bool(witness[1])
            h3 = bool(witness[2])
            neg_q = not bool(witness[3])
        else:
            h1 = bool(getattr(witness, 'is_short_exact_sequence', False))
            h2 = bool(getattr(witness, 'M_prime_is_artinian', False))
            h3 = bool(getattr(witness, 'M_double_prime_is_artinian', False))
            neg_q = not bool(getattr(witness, 'M_is_artinian', True))
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: 0 -> M' -> M -> M'' -> 0 is a short exact sequence of R-modules",
    "H_2: M' is an Artinian R-module",
    "H_3: M'' is an Artinian R-module",
    "¬Q: M is not an Artinian R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3