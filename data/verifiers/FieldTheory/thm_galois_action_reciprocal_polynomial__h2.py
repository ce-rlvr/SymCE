import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a polynomial f(x).
    """
    # H_1: K is a field
    # We assume the witness is a polynomial over a field (e.g., Q).
    try:
        if hasattr(witness, 'free_symbols') and len(witness.free_symbols) == 1:
            var = list(witness.free_symbols)[0]
        else:
            var = x
        f = Poly(witness, var)
        h1 = True
    except Exception:
        return [False, False, False, False]

    # H_2: f(1) != 0 and f(-1) != 0
    try:
        val1 = sympy.expand(f.eval(1))
        val_minus1 = sympy.expand(f.eval(-1))
        h2 = bool(val1 != 0 and val_minus1 != 0)
    except Exception:
        h2 = False

    # H_3: L is the splitting field of f over K
    # This is a definitional hypothesis that sets up L, so it holds for any valid polynomial.
    try:
        h3 = h1
    except Exception:
        h3 = False

    # ¬Q: The conclusion fails
    # The conclusion holds iff the roots of f pair up as (alpha, 1/alpha).
    # This happens iff f(x) and x^d * f(1/x) are proportional (and d is even).
    try:
        if sympy.expand(f.eval(0)) == 0:
            neg_q = True
        else:
            d = f.degree()
            if d % 2 != 0:
                neg_q = True
            else:
                coeffs = f.all_coeffs()
                rev_coeffs = coeffs[::-1]
                c_d = coeffs[0]
                c_0 = coeffs[-1]
                
                is_prop = True
                for c, rc in zip(coeffs, rev_coeffs):
                    diff = sympy.expand(c * c_0 - rc * c_d)
                    if diff != 0:
                        is_prop = False
                        break
                neg_q = not is_prop
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f(1) != 0 and f(-1) != 0",
    "H_3: L is the splitting field of f over K",
    "¬Q: The roots of f do not pair up as (alpha, 1/alpha), so the Galois group does not embed into the hyperoctahedral group"
]

N_HYP = 3
NEG_Q_INDEX = 3