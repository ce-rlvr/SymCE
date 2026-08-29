import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    
    Conjecture: Let K be a field of characteristic zero. 
                The group of units of A_1(K) is exactly K^\\times.
    """
    # H_1: K is a field of characteristic zero
    h1_ok = False
    try:
        is_field = False
        if hasattr(witness, 'is_Field'):
            is_field = bool(witness.is_Field)
        elif hasattr(witness, 'is_field'):
            is_field = bool(witness.is_field)
            
        char_zero = False
        if hasattr(witness, 'characteristic'):
            char_zero = (witness.characteristic == 0)
        elif witness in [sympy.QQ, sympy.RR, sympy.CC]:
            char_zero = True
            is_field = True
            
        if is_field and char_zero:
            h1_ok = True
    except Exception:
        pass

    # ¬Q: The group of units of A_1(K) is NOT exactly K^\times
    # Mathematically, for any commutative ring K, the units of the Weyl algebra A_1(K) 
    # are exactly K^\times if and only if K is reduced (has no nilpotent elements).
    # For any field (or integral domain), K is reduced, so the units are ALWAYS exactly K^\times.
    # Thus, the conclusion is true (and ¬Q is False) for all fields.
    neg_q_ok = False
    try:
        is_reduced = True
        if hasattr(witness, 'is_Field') and witness.is_Field:
            is_reduced = True
        elif hasattr(witness, 'is_field') and witness.is_field:
            is_reduced = True
        elif hasattr(witness, 'is_IntegralDomain') and witness.is_IntegralDomain:
            is_reduced = True
        elif witness in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
            is_reduced = True
        else:
            # If the witness is a ring with nilpotents, it is not reduced.
            if hasattr(witness, 'is_reduced'):
                is_reduced = bool(witness.is_reduced)
                
        neg_q_ok = not is_reduced
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic zero",
    "¬Q: The group of units of A_1(K) is not exactly K^\\times"
]

N_HYP = 1
NEG_Q_INDEX = 1