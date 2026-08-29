import sympy as sp
import math

# Top-level setup
# (No specific named objects required for this domain)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be either the dimension n (an integer) or a point x in U (a tuple of numbers).
    """
    try:
        if isinstance(witness, int) and not isinstance(witness, bool):
            n = witness
            # H1: n is a valid dimension for R^n
            h1 = n >= 0
            # H2: U is the strictly positive orthant (always well-defined for any n)
            h2 = True
        else:
            x = tuple(witness)
            n = len(x)
            # H1: x is a point in R^n
            h1 = all((isinstance(xi, (int, float)) and not isinstance(xi, bool)) or hasattr(xi, 'is_real') for xi in x)
            # H2: x is in the strictly positive orthant U
            h2 = all(xi > 0 for xi in x)
    except Exception:
        return [False, False, False]
        
    try:
        # Conclusion: f is continuously differentiable on U and its partial derivative matches.
        # If n == 0, the geometric mean f() = 1**(1/0) is undefined, so it is not continuously differentiable.
        # For all n >= 1, the function is smooth on U and the partial derivative formula mathematically holds.
        if n == 0:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is a function from R^n to R",
    "H_2: U is the strictly positive orthant",
    "¬Q: f is not continuously differentiable on U or its partial derivative does not match"
]

N_HYP = 2
NEG_Q_INDEX = 2