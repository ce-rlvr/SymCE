import sympy
from sympy import *
import sympy.combinatorics.named_groups
import sympy.matrices
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
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The conjecture drops the "R is commutative" hypothesis from Krull's Intersection Theorem.
    Since SymPy does not natively support non-commutative Noetherian domains, 
    the witness is expected to be a mock object or dictionary representing such a ring.
    """
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        # 1. Dictionary representation
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_noetherian', witness.get('is_Noetherian', False)))
            h2 = bool(witness.get('is_integral_domain', witness.get('is_domain', False)))
            h3 = bool(witness.get('is_proper_ideal', witness.get('proper_ideal', False)))
            
            if 'intersection_zero' in witness:
                neg_q = not bool(witness['intersection_zero'])
            elif 'intersection_is_zero' in witness:
                neg_q = not bool(witness['intersection_is_zero'])
            else:
                neg_q = False
            return [h1, h2, h3, neg_q]
            
        # 2. Tuple representation: (Ring, Ideal)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            h1 = bool(getattr(R, 'is_noetherian', getattr(R, 'is_Noetherian', False)))
            h2 = bool(getattr(R, 'is_integral_domain', getattr(R, 'is_domain', False)))
            h3 = bool(getattr(I, 'is_proper_ideal', getattr(I, 'is_proper', False)))
            
            if hasattr(I, 'intersection_zero'):
                neg_q = not bool(I.intersection_zero)
            elif hasattr(R, 'intersection_zero'):
                neg_q = not bool(R.intersection_zero)
            else:
                neg_q = False
            return [h1, h2, h3, neg_q]

        # 3. Object with R and I attributes
        if hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
            h1 = bool(getattr(R, 'is_noetherian', getattr(R, 'is_Noetherian', False)))
            h2 = bool(getattr(R, 'is_integral_domain', getattr(R, 'is_domain', False)))
            h3 = bool(getattr(I, 'is_proper_ideal', getattr(I, 'is_proper', False)))
            
            if hasattr(witness, 'intersection_zero'):
                neg_q = not bool(witness.intersection_zero)
            elif hasattr(I, 'intersection_zero'):
                neg_q = not bool(I.intersection_zero)
            else:
                neg_q = False
            return [h1, h2, h3, neg_q]

        # 4. Flat object attribute access
        h1 = bool(getattr(witness, 'is_noetherian', getattr(witness, 'is_Noetherian', False)))
        h2 = bool(getattr(witness, 'is_integral_domain', getattr(witness, 'is_domain', False)))
        h3 = bool(getattr(witness, 'is_proper_ideal', getattr(witness, 'proper_ideal', False)))
        
        if hasattr(witness, 'intersection_zero'):
            neg_q = not bool(witness.intersection_zero)
        elif hasattr(witness, 'intersection_is_zero'):
            neg_q = not bool(witness.intersection_is_zero)
        else:
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: R is an integral domain",
    "H_3: I is a proper ideal of R",
    "¬Q: The intersection of I^n is not the zero ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3