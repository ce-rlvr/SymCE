import sympy
from sympy import Symbol, integrate, Abs, oo, nan, zoo
from sympy.abc import x, y, z, t

# Top-level setup
# (No specific algebraic structures needed for this real analysis theorem, 
# but standard variables are provided for witness expressions)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    Expected witness format: (f, (x, a, b))
    where f is a sympy expression, x is the variable, and a, b are the limits.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f, domain = witness
            if isinstance(domain, tuple) and len(domain) == 3:
                x_sym, a, b = domain
                if isinstance(x_sym, Symbol):
                    h1 = True
                else:
                    h1 = False
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    if not h1:
        return [False, False]

    try:
        int_f = integrate(f, (x_sym, a, b))
        int_abs_f = integrate(Abs(f), (x_sym, a, b))
        
        # If the integral of |f| is undefined, the inequality fails.
        if int_abs_f.has(nan) or int_abs_f.has(zoo):
            neg_q = True
        # If the integral of f is undefined, the LHS is undefined, so the inequality fails.
        elif int_f.has(nan) or int_f.has(zoo):
            neg_q = True
        # If int |f| is infinity, the Lebesgue integral of f is only defined if it is +oo or -oo.
        # If sympy returns a finite value (like principal value or improper Riemann integral),
        # the Lebesgue integral is actually undefined, so the inequality fails in the Lebesgue sense.
        elif int_abs_f == oo:
            if int_f != oo and int_f != -oo:
                neg_q = True
            else:
                neg_q = False
        else:
            # Both integrals are finite. Check if |int f| <= int |f|
            diff = int_abs_f - Abs(int_f)
            if diff.is_negative:
                neg_q = True
            elif diff.is_nonnegative:
                neg_q = False
            else:
                # Fallback to numerical evaluation if symbolic comparison fails
                val_f = float(Abs(int_f).evalf())
                val_abs_f = float(int_abs_f.evalf())
                neg_q = not (val_f <= val_abs_f + 1e-9)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (Omega, Sigma, mu) is a measure space",
    "¬Q: The inequality |int f| <= int |f| fails (e.g., integral is undefined)"
]

N_HYP = 1
NEG_Q_INDEX = 1