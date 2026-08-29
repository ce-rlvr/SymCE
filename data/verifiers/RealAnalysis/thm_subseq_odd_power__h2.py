import math
import itertools
import functools
import sympy
from sympy import Rational, Integer, Symbol, symbols

# Top-level setup
# (No specific algebraic structures needed for this real analysis theorem)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (x, L, k) where:
      - x is a list/tuple representing a periodic sequence of real numbers, or a callable x(n)
      - L is a real number
      - k is an integer
    """
    try:
        x, L, k = witness
    except Exception:
        return [False, False, False]
    
    # H1: (x_n) is a sequence of real numbers
    h1 = False
    S_list = []
    try:
        if callable(x):
            for n in range(1, 101):
                S_list.append(float(x(n)))
            h1 = True
        else:
            # Try to iterate over x (e.g., if it's a list or tuple)
            iterator = iter(x)
            for i in range(100):
                try:
                    val = next(iterator)
                    S_list.append(float(val))
                except StopIteration:
                    break
            if len(S_list) > 0:
                h1 = True
    except Exception:
        h1 = False

    # H2: L is a real number
    h2 = False
    try:
        L_float = float(L)
        h2 = True
    except Exception:
        h2 = False

    # neg_Q: The conclusion FAILS
    # Conclusion: L is a subsequential limit of (x_n^k) iff L^{1/k} is a subsequential limit of (x_n)
    neg_q = False
    try:
        if h1 and h2:
            k_int = int(k)
            if k_int != 0:
                # Check if L is a subsequential limit of x_n^k
                left_side = any(abs(L_float - (v**k_int)) < 1e-7 for v in S_list)
                
                # Check if L^{1/k} is a subsequential limit of x_n
                if L_float < 0 and k_int % 2 == 0:
                    # No real k-th root exists for negative L when k is even
                    right_side = False
                else:
                    if L_float < 0:
                        root = - ((-L_float)**(1.0/k_int))
                    else:
                        root = L_float**(1.0/k_int)
                    right_side = any(abs(root - v) < 1e-7 for v in S_list)
                    
                # The conclusion fails if the equivalence does not hold
                neg_q = (left_side != right_side)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (x_n) is a sequence of real numbers",
    "H_2: L is a real number",
    "¬Q: The equivalence between L being a subsequential limit of (x_n^k) and L^{1/k} being a subsequential limit of (x_n) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2