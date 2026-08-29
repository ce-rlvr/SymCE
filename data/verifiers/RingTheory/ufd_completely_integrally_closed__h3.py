import sympy
from sympy import ZZ, QQ, Rational
from sympy.abc import x, y, z

# Top-level setup
# ZZ and QQ are provided for constructing witnesses.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                R, x_val = witness
                K_wit = None
            elif len(witness) == 3:
                R, K_wit, x_val = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        K = None
        if hasattr(R, 'get_field'):
            try:
                K = R.get_field()
            except Exception:
                pass
        if K is None and hasattr(R, 'frac_field'):
            try:
                if callable(R.frac_field):
                    K = R.frac_field()
                else:
                    K = R.frac_field
            except Exception:
                pass
                
        if K_wit is not None and K != K_wit:
            K = None
            
    except Exception:
        R, K, x_val = None, None, None

    # H1: R is a Unique Factorization Domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False

    # H2: K is the field of fractions of R, and x is in K
    try:
        if K is not None:
            try:
                in_K = (x_val in K)
            except Exception:
                in_K = False
            
            if not in_K:
                try:
                    K.from_sympy(sympy.sympify(x_val))
                    in_K = True
                except Exception:
                    in_K = False
            h2 = in_K
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: x does not belong to R
    try:
        if R is not None:
            try:
                in_R = (x_val in R)
            except Exception:
                in_R = False
            
            if not in_R:
                try:
                    R.from_sympy(sympy.sympify(x_val))
                    in_R = True
                except Exception:
                    in_R = False
            neg_q = not in_R
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: K is the field of fractions of R and x is in K",
    "¬Q: x does not belong to R"
]

N_HYP = 2
NEG_Q_INDEX = 2