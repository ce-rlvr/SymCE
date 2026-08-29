import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
# No specific named objects needed for this number theory conjecture.

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: k is a real number",
    "¬Q: \sigma_{-k}(n) != n^{-k} \sigma_k(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    """
    Given a witness (n, k), checks if it is a valid counterexample to the conjecture.
    The conjecture states that \sigma_{-k}(n) = n^{-k} \sigma_k(n).
    """
    try:
        n, k = witness
    except Exception:
        return [False, False, False]

    # H_1: n is a positive integer
    try:
        h1_ok = isinstance(n, int) and n > 0
    except Exception:
        h1_ok = False

    # H_2: k is a real number
    try:
        # Check if k is a real number (int, float, or sympy real)
        h2_ok = isinstance(k, (int, float)) or (hasattr(k, 'is_real') and k.is_real)
    except Exception:
        h2_ok = False

    # ¬Q: \sigma_{-k}(n) != n^{-k} \sigma_k(n)
    try:
        if not h1_ok:
            neg_q = False
        else:
            # Calculate \sigma_k(n)
            divisors = sympy.ntheory.divisors(n)
            
            # Use sympy to handle exact arithmetic if possible
            sigma_k = sum(sympy.Pow(d, k) for d in divisors)
            sigma_minus_k = sum(sympy.Pow(d, -k) for d in divisors)
            
            rhs = sympy.Pow(n, -k) * sigma_k
            
            # Check if they are not equal
            # We simplify the difference to handle symbolic or exact representations
            diff = sympy.simplify(sigma_minus_k - rhs)
            
            # If diff is not exactly zero, then the conclusion fails (neg_Q is True)
            # We also handle floating point comparisons if k is a float
            if isinstance(diff, sympy.Expr):
                neg_q = not diff.is_zero
            else:
                neg_q = not math.isclose(float(sigma_minus_k), float(rhs), rel_tol=1e-9, abs_tol=1e-9)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]