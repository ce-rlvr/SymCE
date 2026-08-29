import sympy
from sympy import *
import math
import itertools
import functools

# Top-level setup
# We define standard symbols. The witness for this ring theory conjecture 
# is expected to be a tuple (m, R_elements, I_elements, x) representing 
# a subring R of Z_m, an ideal I of R, and an element x in Z_m.
x_sym, y_sym, z_sym = symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that x must be an element of R.
    """
    try:
        # Parse witness
        if isinstance(witness, dict):
            m = witness['m']
            R_list = witness['R']
            I_list = witness['I']
            x_val = witness['x']
        else:
            m, R_list, I_list, x_val = witness
            
        m = int(m)
        if m < 1:
            return [False, False, False]
            
        R = set(int(r) % m for r in R_list)
        I = set(int(i) % m for i in I_list)
        x_val = int(x_val) % m
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring
    # We check if R is a valid subring of Z_m (which is automatically commutative)
    try:
        h1 = False
        if R:
            is_subring = True
            for a in R:
                if (-a) % m not in R:
                    is_subring = False
                    break
                for b in R:
                    if (a + b) % m not in R:
                        is_subring = False
                        break
                    if (a * b) % m not in R:
                        is_subring = False
                        break
                if not is_subring:
                    break
            h1 = is_subring
    except Exception:
        h1 = False

    # H_2: I is an ideal of R
    try:
        h2 = False
        if I and I.issubset(R):
            is_ideal = True
            for i in I:
                if (-i) % m not in I:
                    is_ideal = False
                    break
                for j in I:
                    if (i + j) % m not in I:
                        is_ideal = False
                        break
                for r in R:
                    if (i * r) % m not in I:
                        is_ideal = False
                        break
                if not is_ideal:
                    break
            h2 = is_ideal
    except Exception:
        h2 = False

    # neg_Q: The equivalence fails
    # Conclusion: x + I is nilpotent in R/I iff exists n > 0 such that x^n \in I
    try:
        # RHS: exists n > 0 such that x^n \in I
        rhs = False
        curr = x_val % m
        for _ in range(m + 2):
            if curr in I:
                rhs = True
                break
            curr = (curr * x_val) % m
            
        # LHS: x + I is a nilpotent element in R/I
        # For x + I to be an element of R/I, x must be in R.
        # If x is in R, (x+I)^n = x^n + I, so it is nilpotent iff x^n \in I.
        lhs = (x_val in R) and rhs
        
        # The conjecture fails if the LHS and RHS of the iff statement do not match
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The equivalence between x+I being nilpotent and x^n in I fails (e.g., x is not in R)"
]

N_HYP = 2
NEG_Q_INDEX = 2