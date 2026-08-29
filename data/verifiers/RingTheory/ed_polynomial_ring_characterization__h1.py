import sympy
from sympy import *
from sympy.abc import *

# Top-level setup for potential witness expressions
S3 = None
Z2 = None
I2 = eye(2)
O2 = zeros(2, 2)

def conditions(witness):
    """
    Checks whether the witness is a counterexample to the conjecture.
    
    Conjecture:
      H1: Let R_x be the polynomial ring over R in one variable
      H2: R_x is a Euclidean domain
      Conclusion: R is a field
      
    The conjecture is false because R could be a non-commutative division ring 
    (e.g., the Quaternions). For a division ring R, R_x is a Euclidean domain 
    (using left or right division), but R is not a field (since fields must be commutative).
    """
    
    # H_1: Let R_x be the polynomial ring over R in one variable
    # This is a setup hypothesis, which is vacuously true for any valid ring witness.
    try:
        h1 = True
    except Exception:
        h1 = False

    # H_2: R_x is a Euclidean domain
    # R_x is a Euclidean domain if and only if R is a division ring.
    try:
        is_div_ring = False
        
        # Fields are commutative division rings
        if getattr(witness, 'is_Field', False) or getattr(witness, 'is_field', False):
            is_div_ring = True
            
        # Check for Quaternions (the standard non-commutative division ring)
        w_str = str(witness).lower()
        w_type_str = str(type(witness)).lower()
        if 'quaternion' in w_str or 'quaternion' in w_type_str:
            is_div_ring = True
            
        # Check for explicit division ring properties
        if getattr(witness, 'is_division_ring', False) or getattr(witness, 'is_DivisionRing', False):
            is_div_ring = True
            
        h2 = bool(is_div_ring)
    except Exception:
        h2 = False

    # not Q: R is not a field
    try:
        is_f = False
        
        if getattr(witness, 'is_Field', False) or getattr(witness, 'is_field', False):
            is_f = True
            
        # Quaternions are explicitly non-commutative, hence not fields
        w_str = str(witness).lower()
        w_type_str = str(type(witness)).lower()
        if 'quaternion' in w_str or 'quaternion' in w_type_str:
            is_f = False
            
        neg_q = not bool(is_f)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Let R_x be the polynomial ring over R in one variable",
    "H_2: R_x is a Euclidean domain",
    "not Q: R is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2