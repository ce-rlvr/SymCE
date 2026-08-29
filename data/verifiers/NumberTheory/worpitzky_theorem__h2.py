import math
import itertools
import functools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# No specific named bindings required for this Number Theory conjecture.

def get_val(witness, n):
    """
    Evaluates the sequence at index n (1-indexed).
    Supports both callable functions and subscriptable iterables.
    """
    if callable(witness):
        return complex(witness(n))
    elif hasattr(witness, '__getitem__'):
        idx = (n - 1) % len(witness)
        return complex(witness[idx])
    else:
        raise ValueError("Witness must be callable or subscriptable")

def conditions(witness) -> list[bool]:
    # H_1: (a_n) is a sequence of complex numbers
    try:
        h1 = False
        for i in range(1, 1001):
            val = get_val(witness, i)
            if math.isnan(val.real) or math.isnan(val.imag) or math.isinf(val.real) or math.isinf(val.imag):
                break
        else:
            h1 = True
    except Exception:
        h1 = False

    # neg_Q: The continued fraction diverges OR converges to z with |z| > 1/2
    try:
        neg_q = False
        A_prev2, B_prev2 = complex(1, 0), complex(0, 0)
        A_prev1, B_prev1 = complex(0, 0), complex(1, 0)
        S = []
        
        for k in range(1, 1001):
            ak = get_val(witness, k)
            A_k = A_prev1 + ak * A_prev2
            B_k = B_prev1 + ak * B_prev2
            
            # Normalize to prevent overflow/underflow while preserving the ratio
            m = max(abs(A_k), abs(B_k))
            if m > 0:
                A_k /= m
                B_k /= m
                A_prev1 /= m
                B_prev1 /= m
                
            if abs(B_k) > 1e-15:
                S.append(A_k / B_k)
            else:
                S.append(None)
                
            A_prev2, B_prev2 = A_prev1, B_prev1
            A_prev1, B_prev1 = A_k, B_k
            
        converges = False
        valid_S = [val for val in S if val is not None]
        
        if len(valid_S) >= 20:
            last_20 = valid_S[-20:]
            z_val = last_20[-1]
            # Check if the sequence of approximants has stabilized
            if all(abs(val - z_val) < 1e-4 for val in last_20):
                converges = True
                
        if not converges:
            neg_q = True
        else:
            if abs(z_val) > 0.5 + 1e-7:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (a_n) is a sequence of complex numbers",
    "¬Q: The continued fraction diverges or converges to z with |z| > 1/2"
]

N_HYP = 1
NEG_Q_INDEX = 1