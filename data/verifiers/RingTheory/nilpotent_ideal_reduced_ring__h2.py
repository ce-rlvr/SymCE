import sympy
from sympy import *
import itertools

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_lists(R, I):
    R = list(R)
    I = list(I)
    
    def eq(a, b):
        return a == b

    # Find the zero element of the ring R
    zero = None
    for x in R:
        if all(eq(x + y, y) for y in R):
            zero = x
            break
            
    if zero is None:
        return False, False, False
        
    # Check if R is commutative
    is_comm = all(eq(x * y, y * x) for x in R for y in R)
    
    # Check if R is reduced (in a commutative ring, x^2 = 0 implies x = 0 is sufficient)
    is_reduced = all(eq(x, zero) for x in R if eq(x * x, zero))
    
    # Check if R is closed under addition and multiplication
    is_closed = True
    for x in R:
        for y in R:
            if not any(eq(x + y, z) for z in R):
                is_closed = False
            if not any(eq(x * y, z) for z in R):
                is_closed = False
                
    h1 = is_comm and is_reduced and is_closed
    
    # Check if I is an ideal of R
    is_ideal = len(I) > 0
    for x in I:
        if not any(eq(x, z) for z in R):
            is_ideal = False
        for y in I:
            if not any(eq(x + y, z) for z in I):
                is_ideal = False
        for r in R:
            if not any(eq(r * x, z) for z in I):
                is_ideal = False
                
    # Check if I^2 is the zero ideal (i.e., xy = 0 for all x, y in I)
    i_sq_zero = all(eq(x * y, zero) for x in I for y in I)
    h2 = is_ideal and i_sq_zero
    
    # Check if I is the zero ideal
    i_is_zero = all(eq(x, zero) for x in I)
    neg_q = not i_is_zero
    
    return bool(h1), bool(h2), bool(neg_q)

def conditions(witness):
    # Attempt to unpack witness as a tuple of lists/sets (R, I)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if isinstance(R, (list, tuple, set)) and isinstance(I, (list, tuple, set)):
                return list(check_lists(R, I))
    except Exception:
        pass

    # Attempt to unpack witness as a dictionary {'R': ..., 'I': ...}
    try:
        if isinstance(witness, dict) and 'R' in witness and 'I' in witness:
            R = witness['R']
            I = witness['I']
            if isinstance(R, (list, tuple, set)) and isinstance(I, (list, tuple, set)):
                return list(check_lists(R, I))
    except Exception:
        pass

    # Attempt to unpack witness as an object with R and I attributes
    try:
        if hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
            if isinstance(R, (list, tuple, set)) and isinstance(I, (list, tuple, set)):
                return list(check_lists(R, I))
    except Exception:
        pass

    # Fallback for object-based witness with boolean properties
    h1 = False
    try:
        if hasattr(witness, 'is_reduced') and hasattr(witness, 'is_commutative'):
            h1 = bool(witness.is_reduced and witness.is_commutative)
        elif hasattr(witness, 'R_is_reduced') and hasattr(witness, 'R_is_commutative'):
            h1 = bool(witness.R_is_reduced and witness.R_is_commutative)
    except Exception:
        pass
        
    h2 = False
    try:
        if hasattr(witness, 'I_squared_is_zero'):
            h2 = bool(witness.I_squared_is_zero)
    except Exception:
        pass
        
    neg_q = False
    try:
        if hasattr(witness, 'I_is_zero'):
            neg_q = not bool(witness.I_is_zero)
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a reduced commutative ring",
    "H_2: The product of I with itself (I^2) is the zero ideal",
    "¬Q: The ideal I is not the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2