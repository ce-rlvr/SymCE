import sympy as sp
from sympy.abc import n, x
import math

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple: (poly, closed_form)
    where `poly` is the characteristic polynomial of the homogeneous part of the recurrence,
    and `closed_form` is the explicit closed-form formula for a_n.
    
    Example counterexample (non-homogeneous recurrence a_n = 2a_{n-1} + 4^n):
    witness = (x - 2, 2**n + 4**n)
    """
    H1 = False
    H2 = False
    H3 = False
    neg_Q = False

    try:
        poly, closed_form = witness

        # H1: The characteristic polynomial of the recurrence relation has distinct roots
        roots_dict = sp.roots(poly, x)
        degree = sp.degree(poly, x)
        H1 = (sum(roots_dict.values()) == degree) and degree > 0 and all(mult == 1 for mult in roots_dict.values())

        if not H1:
            return [False, False, False, False]

        # H2: lambda is the root with the strictly largest absolute value, and lambda != 0
        roots = list(roots_dict.keys())
        abs_roots = [float(sp.Abs(r)) for r in roots]
        max_abs = max(abs_roots)
        count_max = sum(1 for ar in abs_roots if abs(ar - max_abs) < 1e-9)
        H2 = (count_max == 1)

        if not H2:
            return [H1, False, False, False]

        max_idx = abs_roots.index(max_abs)
        lambda_root = roots[max_idx]
        H2 = H2 and (abs(float(lambda_root)) > 1e-9)

        # H3: The initial conditions are such that the coefficient of lambda^n in the explicit closed-form formula for a_n is non-zero
        expanded = sp.expand(closed_form)
        coeff = expanded.coeff(lambda_root**n)
        
        if coeff == 0:
            dummy = sp.Symbol('dummy_var')
            coeff = expanded.subs(lambda_root**n, dummy).coeff(dummy)
            
        H3 = (coeff != 0)

        # neg_Q: The radius of convergence of the power series is NOT 1/|lambda|
        # The radius of convergence R is given by 1 / limsup |a_n|^(1/n).
        # We approximate limsup |a_n|^(1/n) by evaluating at a large n (e.g., n=10000).
        a_large = sp.Abs(closed_form.subs(n, 10000))
        limsup_approx = float(sp.N(a_large**(sp.Rational(1, 10000))))
        
        # If the conclusion holds, limsup_approx should be very close to |lambda| (max_abs).
        # The negated conclusion means they are significantly different.
        neg_Q = abs(limsup_approx - max_abs) > 1e-2

    except Exception:
        pass

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: The characteristic polynomial of the recurrence relation has distinct roots",
    "H_2: lambda is the root of the characteristic polynomial with the strictly largest absolute value, and lambda != 0",
    "H_3: The initial conditions are such that the coefficient of lambda^n in the explicit closed-form formula for a_n is non-zero",
    "¬Q: The radius of convergence of the power series is NOT 1/|lambda|"
]

N_HYP = 3
NEG_Q_INDEX = 3