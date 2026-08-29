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
    Check if the witness is a valid counterexample to the false conjecture.
    
    Remaining hypotheses:
      - R is a commutative ring
      - J is an ideal of R
    
    Conclusion (must FAIL at the witness):
      dim(R/(IJ)) = max(dim(R/I), dim(R/J))
    """
    h1 = False
    h2 = False
    neg_q = False

    # Approach 1: Witness is a dictionary
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('R_is_commutative', False))
            h2 = bool(witness.get('J_is_ideal', False))
            dim_IJ = witness.get('dim_R_IJ')
            dim_I = witness.get('dim_R_I')
            dim_J = witness.get('dim_R_J')
            if dim_IJ is not None and dim_I is not None and dim_J is not None:
                neg_q = dim_IJ != max(dim_I, dim_J)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # Approach 2: Witness is a mock object with attributes
    try:
        h1 = bool(getattr(witness, 'R_is_commutative', False))
        h2 = bool(getattr(witness, 'J_is_ideal', False))
        dim_IJ = getattr(witness, 'dim_R_IJ', None)
        dim_I = getattr(witness, 'dim_R_I', None)
        dim_J = getattr(witness, 'dim_R_J', None)
        if dim_IJ is not None and dim_I is not None and dim_J is not None:
            neg_q = dim_IJ != max(dim_I, dim_J)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # Approach 3: Witness is a tuple of custom objects (R, I, J)
    try:
        if isinstance(witness, (list, tuple)) and len(witness) == 3:
            R, I, J = witness
            
            # Check H1: R is a commutative ring
            if hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            elif hasattr(R, 'is_commutative_ring'):
                h1 = bool(R.is_commutative_ring())
                
            # Check H2: J is an ideal of R
            if hasattr(J, 'is_ideal'):
                try:
                    h2 = bool(J.is_ideal(R))
                except Exception:
                    h2 = bool(J.is_ideal())
                    
            # Check neg_Q: dim(R/(IJ)) != max(dim(R/I), dim(R/J))
            if hasattr(R, 'quotient'):
                try:
                    dim_IJ = R.quotient(I * J).krull_dimension()
                    dim_I = R.quotient(I).krull_dimension()
                    dim_J = R.quotient(J).krull_dimension()
                    neg_q = dim_IJ != max(dim_I, dim_J)
                except Exception:
                    try:
                        dim_IJ = R.quotient(I.mul(J)).dim()
                        dim_I = R.quotient(I).dim()
                        dim_J = R.quotient(J).dim()
                        neg_q = dim_IJ != max(dim_I, dim_J)
                    except Exception:
                        pass
                        
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "¬Q: dim(R/(IJ)) != max(dim(R/I), dim(R/J))"
]

N_HYP = 2
NEG_Q_INDEX = 2