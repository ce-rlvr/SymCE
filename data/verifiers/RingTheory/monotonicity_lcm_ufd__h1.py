import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_nz(val):
    """Safely check if a value is non-zero."""
    try:
        if hasattr(val, 'is_zero_matrix'):
            return not val.is_zero_matrix
        if hasattr(val, 'is_zero') and val.is_zero is not None:
            return not val.is_zero
        return bool(val != 0)
    except Exception:
        return False

def check_divides(a, b):
    """Safely check if a divides b in various algebraic structures."""
    if hasattr(a, 'divides'):
        try:
            return bool(a.divides(b))
        except Exception:
            pass
            
    try:
        if a == 0:
            return b == 0
    except Exception:
        pass
        
    if isinstance(a, (sympy.Rational, float)) and isinstance(b, (sympy.Rational, float)):
        if a != 0:
            return True
            
    if isinstance(a, sympy.MatrixBase) and isinstance(b, sympy.MatrixBase):
        try:
            # In a matrix ring, a divides b (right divisibility) if a * X = b has a solution.
            # This is true iff the column space of b is a subset of the column space of a.
            if a.rank() == a.row_join(b).rank():
                return True
        except Exception:
            pass
            
    try:
        if sympy.rem(b, a) == 0:
            return True
    except Exception:
        pass
        
    try:
        q = sympy.simplify(b / a)
        if isinstance(q, (int, sympy.Integer)):
            return True
        if getattr(q, 'as_numer_denom', None) is not None:
            if q.as_numer_denom()[1] == 1:
                return True
    except Exception:
        pass
        
    try:
        if b % a == 0:
            return True
    except Exception:
        pass
        
    return False

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok]
    """
    # The witness can either explicitly provide the ring or just be the elements
    if isinstance(witness, (tuple, list)) and len(witness) == 4:
        ring, a, b, c = witness
        
        try:
            h1 = bool(ring.is_non_zero(a) and ring.is_non_zero(b) and ring.is_non_zero(c))
        except Exception:
            h1 = False
            
        try:
            h2 = bool(ring.divides(a, b))
        except Exception:
            h2 = False
            
        try:
            lcm_ac = ring.lcm(a, c)
            lcm_bc = ring.lcm(b, c)
            concl = bool(ring.divides(lcm_ac, lcm_bc))
        except Exception:
            # If LCM doesn't exist or divisibility fails, the conclusion is false
            concl = False
            
    elif isinstance(witness, (tuple, list)) and len(witness) == 3:
        a, b, c = witness
        
        try:
            h1 = is_nz(a) and is_nz(b) and is_nz(c)
        except Exception:
            h1 = False
            
        try:
            h2 = check_divides(a, b)
        except Exception:
            h2 = False
            
        try:
            if hasattr(a, 'lcm'):
                lcm_ac = a.lcm(c)
                lcm_bc = b.lcm(c)
            else:
                lcm_ac = sympy.lcm(a, c)
                lcm_bc = sympy.lcm(b, c)
                
            concl = check_divides(lcm_ac, lcm_bc)
        except Exception:
            # If sympy.lcm raises an exception (e.g., for matrices or non-UFD elements),
            # the LCM does not exist, meaning the conclusion statement fails.
            concl = False
            
    else:
        return [False, False, False]

    neg_q = not concl
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c are non-zero elements of R",
    "H_2: a divides b",
    "¬Q: lcm(a, c) does not divide lcm(b, c)"
]

N_HYP = 2
NEG_Q_INDEX = 2