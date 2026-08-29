import sympy
from sympy import Matrix, Poly, simplify, eye, zeros
from sympy.abc import x

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def eval_poly_matrix(poly_expr, var, mat):
    poly = Poly(poly_expr, var)
    n = mat.shape[0]
    res = sympy.zeros(n, n)
    for power, coeff in poly.as_dict().items():
        res += coeff * (mat ** power[0])
    return res

def conditions(witness) -> list[bool]:
    try:
        p, C = witness
    except Exception:
        return [False, False]
        
    # H1: p(x) is a monic polynomial of degree n >= 1
    h1 = False
    try:
        p = sympy.sympify(p)
        symbols = p.free_symbols
        if len(symbols) == 1:
            var = list(symbols)[0]
        elif len(symbols) == 0:
            var = x
        else:
            if x in symbols:
                var = x
            else:
                var = sorted(list(symbols), key=lambda s: s.name)[0]
            
        if var is not None:
            poly_p = Poly(p, var)
            h1 = bool(poly_p.is_monic and poly_p.degree() >= 1)
    except Exception:
        h1 = False

    # neg_Q: The characteristic polynomial of C is not p(x) OR the minimal polynomial of C is not p(x)
    neg_q = False
    try:
        if not isinstance(C, Matrix) or not C.is_square:
            neg_q = True
        else:
            if var is None:
                var = x
            char_poly = C.charpoly(var).as_expr()
            char_eq = simplify(char_poly - p) == 0
            
            if not char_eq:
                neg_q = True
            else:
                # If char_poly == p, then min_poly divides p.
                # min_poly == p iff (p/f)(C) != 0 for all irreducible factors f of p.
                min_eq = True
                factors = sympy.factor_list(p)[1]
                for f, mult in factors:
                    q_expr = simplify(p / f)
                    q_mat = eval_poly_matrix(q_expr, var, C)
                    is_zero = all(simplify(e) == 0 for e in q_mat)
                    if is_zero:
                        min_eq = False
                        break
                neg_q = not min_eq
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p(x) is a monic polynomial of degree n >= 1",
    "¬Q: The characteristic polynomial of C is not p(x) or the minimal polynomial of C is not p(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1