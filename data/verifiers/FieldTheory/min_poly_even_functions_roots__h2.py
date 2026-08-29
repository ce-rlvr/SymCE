import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
O0 = zeros(0, 0)

def conditions(witness):
    x = sympy.Symbol('x')
    
    def eval_poly(poly, mat):
        if mat.shape == (0, 0):
            return sympy.zeros(0, 0)
        res = sympy.zeros(mat.shape[0], mat.shape[1])
        I = sympy.eye(mat.shape[0])
        coeffs = poly.all_coeffs()
        degree = len(coeffs) - 1
        for i, c in enumerate(coeffs):
            power = degree - i
            if power == 0:
                res += c * I
            else:
                res += c * (mat ** power)
        return res

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            alpha, min_poly_expr = witness
        else:
            alpha = witness
            if hasattr(alpha, 'is_Matrix') and alpha.is_Matrix:
                if alpha.shape == (0, 0):
                    min_poly_expr = sympy.Integer(1)
                else:
                    min_poly_expr = alpha.charpoly(x).as_expr()
            else:
                min_poly_expr = sympy.minimal_polynomial(alpha, x)
    except Exception:
        return [False, False, False]

    # H_1: F is a field of characteristic not equal to 2
    # We evaluate over QQ or CC (characteristic 0), so this holds.
    h1 = True

    # H_2: The minimal polynomial of alpha over F is of the form g(x^2)
    h2 = False
    p = None
    try:
        p = sympy.Poly(min_poly_expr, x)
        if p.is_monic:
            is_min = False
            if hasattr(alpha, 'is_Matrix') and alpha.is_Matrix:
                if eval_poly(p, alpha) == sympy.zeros(*alpha.shape):
                    is_min = True
                    factors = sympy.factor_list(p)[1]
                    for factor, _ in factors:
                        q = p.quo(sympy.Poly(factor, x))
                        if eval_poly(q, alpha) == sympy.zeros(*alpha.shape):
                            is_min = False
                            break
            else:
                expected = sympy.minimal_polynomial(alpha, x)
                is_min = p.as_expr().equals(expected)
            
            if is_min:
                coeffs = p.all_coeffs()
                degree = len(coeffs) - 1
                h2 = True
                for i, c in enumerate(coeffs):
                    power = degree - i
                    if power % 2 != 0 and c != 0:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # Negated Conclusion: -alpha is not a root of the minimal polynomial, or alpha == 0
    neg_q = False
    try:
        if p is not None:
            if hasattr(alpha, 'is_Matrix') and alpha.is_Matrix:
                neg_alpha = -alpha
                is_root = (eval_poly(p, neg_alpha) == sympy.zeros(*alpha.shape))
                is_zero = (alpha == sympy.zeros(*alpha.shape))
                neg_q = bool((not is_root) or is_zero)
            else:
                neg_alpha = -alpha
                val = p.as_expr().subs(x, neg_alpha)
                is_root = (sympy.simplify(val) == 0)
                is_zero = (alpha == 0)
                neg_q = bool((not is_root) or is_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: The minimal polynomial of alpha over F is of the form g(x^2)",
    "not Q: -alpha is not a root of the minimal polynomial, or alpha == 0"
]

N_HYP = 2
NEG_Q_INDEX = 2