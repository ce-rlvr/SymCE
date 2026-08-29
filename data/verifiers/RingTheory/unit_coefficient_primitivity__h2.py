import sympy
from sympy import Poly, Expr
from sympy.abc import x, y, z

# Top-level setup for witness expressions
# Variables x, y, z are available for constructing polynomials.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    """
    # Ensure the witness is a SymPy Poly object
    try:
        if isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness)
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        R = f.domain
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False

    # H_2: At least one coefficient of f is a unit in R
    try:
        coeffs = f.coeffs()
        R = f.domain
        h2 = False
        for c in coeffs:
            try:
                is_u = False
                # 1. Try the domain's native is_unit method
                if hasattr(R, 'is_unit'):
                    try:
                        is_u = bool(R.is_unit(c))
                    except Exception:
                        pass
                # 2. Fallback for fields (all non-zero elements are units)
                if not is_u and getattr(R, 'is_Field', False) and c != R.zero:
                    is_u = True
                # 3. Fallback for integers (1 and -1 are units)
                if not is_u and getattr(R, 'is_ZZ', False) and abs(c) == 1:
                    is_u = True
                # 4. General fallback: check if c divides 1
                if not is_u:
                    try:
                        if R.exquo(R.one, c):
                            is_u = True
                    except Exception:
                        pass
                
                if is_u:
                    h2 = True
                    break
            except Exception:
                continue
    except Exception:
        h2 = False

    # ¬Q: The polynomial f is NOT primitive
    # (In strict algebraic contexts and SymPy, a polynomial is primitive iff its content is exactly 1.
    # A polynomial with a unit coefficient might have a unit content other than 1, e.g., -1 in ZZ,
    # making it non-primitive under the strict definition.)
    try:
        neg_q = not bool(f.is_primitive)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: At least one coefficient of f is a unit in R",
    "¬Q: The polynomial f is not primitive"
]

N_HYP = 2
NEG_Q_INDEX = 2