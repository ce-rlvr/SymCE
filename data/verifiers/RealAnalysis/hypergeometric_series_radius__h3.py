import sympy
import math

# Top-level setup
# (No specific named objects required for this domain)

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False]
    
    # H1: a, b, c are real numbers
    try:
        h1 = all(complex(x).imag == 0.0 for x in (a, b, c))
    except Exception:
        h1 = False
        
    # H2: c is not a non-positive integer
    try:
        c_val = float(c)
        h2 = not (c_val <= 0 and c_val.is_integer())
    except Exception:
        h2 = False
        
    # neg_Q: The radius of convergence is NOT exactly 1
    # The radius of convergence is exactly 1 unless the series terminates.
    # The series terminates if and only if a or b is a non-positive integer,
    # in which case it becomes a polynomial and the radius of convergence is infinity.
    try:
        a_val = float(a)
        a_terminates = (a_val <= 0 and a_val.is_integer())
        
        b_val = float(b)
        b_terminates = (b_val <= 0 and b_val.is_integer())
        
        neg_q = a_terminates or b_terminates
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c are real numbers",
    "H_2: c is not a non-positive integer",
    "¬Q: The radius of convergence of the power series is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2