import sympy
from sympy import Poly, Symbol, Rational, Integer
from sympy.abc import x, y, z
from sympy import ZZ, QQ
from sympy.ntheory import factorint

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain (UFD)",
    "H_2: F is the field of fractions of R",
    "H_3: f(x) is reducible over F",
    "not Q: f(x) is not reducible over R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (R, f) or (R, F, f) where:
      - R is a sympy Domain (e.g., ZZ)
      - f is a sympy expression representing the polynomial f(x)
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                R, f = witness
                F_wit = None
            elif len(witness) == 3:
                R, F_wit, f = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a Unique Factorization Domain (UFD)
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    # H_2: F is the field of fractions of R
    try:
        F = R.get_field()
        h2 = bool(getattr(F, 'is_Field', False))
        if F_wit is not None:
            h2 = h2 and (F == F_wit)
    except Exception:
        h2 = False

    # H_3: f(x) is reducible over F[x]
    try:
        if not h2:
            F = QQ # fallback just in case
        
        free_symbols = f.free_symbols
        if len(free_symbols) != 1:
            h3 = False
        else:
            var = list(free_symbols)[0]
            poly_F = Poly(f, var, domain=F)
            _, factors = poly_F.factor_list()
            # A polynomial is reducible over a field if it factors into >= 2 non-constant polynomials
            num_non_constant_factors = sum(mult for fac, mult in factors if fac.degree() >= 1)
            h3 = num_non_constant_factors >= 2
    except Exception:
        h3 = False

    # ¬Q: f(x) is NOT reducible over R[x]
    try:
        free_symbols = f.free_symbols
        if len(free_symbols) != 1:
            neg_q = False
        else:
            var = list(free_symbols)[0]
            poly_R = Poly(f, var)
            coeffs = poly_R.coeffs()
            
            # Check if f(x) is in R[x]
            in_R = True
            for c in coeffs:
                if c not in R:
                    in_R = False
                    break
            
            if not in_R:
                # If f(x) is not in R[x], it cannot be reducible over R[x]
                reducible_over_R = False
            else:
                poly_R_domain = Poly(f, var, domain=R)
                coeff, factors = poly_R_domain.factor_list()
                
                # Count non-unit factors in R[x]
                num_poly_factors = 0
                for fac, mult in factors:
                    if fac.degree() >= 1:
                        num_poly_factors += mult
                    else:
                        # constant factor
                        c_val = fac.as_expr()
                        if not R.is_unit(c_val):
                            if R == ZZ:
                                try:
                                    pf = factorint(abs(int(c_val)))
                                    num_poly_factors += sum(pf.values()) * mult
                                except Exception:
                                    num_poly_factors += mult
                            else:
                                num_poly_factors += mult
                
                # Also consider the leading coefficient `coeff`
                if not R.is_unit(coeff):
                    if R == ZZ:
                        try:
                            pf = factorint(abs(int(coeff)))
                            num_poly_factors += sum(pf.values())
                        except Exception:
                            num_poly_factors += 1
                    else:
                        num_poly_factors += 1
                        
                # Reducible in R[x] means it can be factored into >= 2 non-units
                reducible_over_R = num_poly_factors >= 2

            neg_q = not reducible_over_R
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]