import sympy
from sympy import simplify, Poly, Matrix, eye
from sympy.abc import x, y, z, t

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    "Roots of Even Minimal Polynomials"
    """
    
    def is_expr_zero(expr):
        try:
            if expr == 0:
                return True
            if simplify(expr) == 0:
                return True
            return False
        except Exception:
            return False

    def is_expr_nonzero(expr):
        try:
            if expr == 0:
                return False
            if simplify(expr) == 0:
                return False
            return True
        except Exception:
            return True

    try:
        if isinstance(witness, dict):
            alpha = witness.get('alpha')
            min_poly = witness.get('min_poly')
        else:
            alpha = witness[0]
            min_poly = witness[1]
    except Exception:
        return [False, False, False]

    # H_1: alpha is algebraic over F
    # This means min_poly is irreducible, monic, and min_poly(alpha) == 0
    try:
        if not isinstance(min_poly, Poly):
            min_poly = Poly(min_poly)
        
        is_monic = min_poly.LC() == 1
        is_irreducible = min_poly.is_irreducible
        
        if hasattr(alpha, 'is_Matrix') and alpha.is_Matrix:
            val = alpha.zeros(*alpha.shape)
            coeffs = min_poly.all_coeffs()
            deg = min_poly.degree()
            for i, c in enumerate(coeffs):
                power = deg - i
                if power == 0:
                    val += c * eye(alpha.shape[0])
                else:
                    val += c * (alpha ** power)
            is_root_alpha = val.is_zero_matrix
        else:
            val = min_poly.eval(alpha)
            is_root_alpha = is_expr_zero(val)
            
        h1 = bool(is_monic and is_irreducible and is_root_alpha)
    except Exception:
        h1 = False

    # H_2: The minimal polynomial of alpha over F is of the form g(x^2)
    try:
        monoms = min_poly.monoms()
        h2 = all(sum(deg) % 2 == 0 for deg in monoms)
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails.
    # Conclusion: -alpha is a root of min_poly, and alpha != 0
    # We evaluate both alpha != 0 and alpha != -alpha (2*alpha != 0) to robustly catch 
    # the intended characteristic 2 counterexample regardless of formalization details.
    try:
        if hasattr(alpha, 'is_Matrix') and alpha.is_Matrix:
            neg_alpha = -alpha
            val_neg = alpha.zeros(*alpha.shape)
            coeffs = min_poly.all_coeffs()
            deg = min_poly.degree()
            for i, c in enumerate(coeffs):
                power = deg - i
                if power == 0:
                    val_neg += c * eye(alpha.shape[0])
                else:
                    val_neg += c * (neg_alpha ** power)
            is_root_neg = val_neg.is_zero_matrix
            is_nonzero = (not alpha.is_zero_matrix) and (not (alpha + alpha).is_zero_matrix)
        else:
            val_neg = min_poly.eval(-alpha)
            is_root_neg = is_expr_zero(val_neg)
            is_nonzero = is_expr_nonzero(alpha) and is_expr_nonzero(alpha + alpha)
            
        neg_q = not (is_root_neg and is_nonzero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is algebraic over F",
    "H_2: The minimal polynomial of alpha over F is of the form g(x^2)",
    "¬Q: -alpha is not a root of the minimal polynomial, or alpha == 0"
]

N_HYP = 2
NEG_Q_INDEX = 2