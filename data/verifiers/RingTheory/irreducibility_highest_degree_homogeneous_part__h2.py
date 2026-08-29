import sympy
from sympy import symbols, Poly, factor_list
from sympy.abc import x, y

# Top-level setup
# We will evaluate the witness as a tuple: (K, f)
# where K is a sympy Domain (e.g., sympy.QQ) and f is a sympy Expr in x, y.

def conditions(witness) -> list[bool]:
    try:
        K, f = witness
    except Exception:
        return [False, False, False, False]

    # H_1: K is a field
    try:
        h1 = K.is_Field
    except Exception:
        h1 = False

    # H_2: f(x,y) = f_n + ... + f_0 where f_i is homogeneous of degree i
    try:
        poly_f = Poly(f, x, y, domain=K)
        terms = poly_f.terms()
        h2 = True
    except Exception:
        h2 = False

    # H_3: f_n(x,y) is irreducible in K[x,y]
    try:
        if not poly_f.is_zero:
            n = poly_f.total_degree()
            f_n_expr = sum(coeff * (x**monom[0]) * (y**monom[1]) for monom, coeff in terms if sum(monom) == n)
            f_n_poly = Poly(f_n_expr, x, y, domain=K)
            
            const, factors = factor_list(f_n_poly)
            if len(factors) == 1 and factors[0][1] == 1 and Poly(factors[0][0], x, y).total_degree() > 0:
                h3 = True
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: f(x,y) is NOT irreducible in K[x,y]
    try:
        const_f, factors_f = factor_list(poly_f)
        is_irreducible = (len(factors_f) == 1 and factors_f[0][1] == 1 and Poly(factors_f[0][0], x, y).total_degree() > 0)
        neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is a sum of homogeneous polynomials",
    "H_3: f_n is irreducible",
    "¬Q: f is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3