import sympy
from sympy import Poly, Matrix, zeros, eye
from sympy.abc import x

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    try:
        F = witness.get('F')
        alpha = witness.get('alpha')
        m = witness.get('m')
        x_sym = witness.get('x', x)
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    try:
        p = Poly(m, x_sym, domain=F)
        if p.is_zero:
            h2 = False
        else:
            if hasattr(alpha, 'shape'):
                n = alpha.shape[0]
                val = zeros(n, n)
                coeffs = p.all_coeffs()
                deg = p.degree()
                for i, c in enumerate(coeffs):
                    val += c * (alpha ** (deg - i))
                h2 = bool(val == zeros(n, n))
            else:
                h2 = bool(sympy.simplify(p.eval(alpha)) == 0)
                if not h2:
                    h2 = bool(getattr(alpha, 'is_algebraic', False))
    except Exception:
        h2 = False

    try:
        p = Poly(m, x_sym, domain=F)
        if not p.is_monic or p.is_zero:
            h3 = False
        else:
            deg = p.degree()
            if hasattr(alpha, 'shape'):
                n = alpha.shape[0]
                val = zeros(n, n)
                coeffs = p.all_coeffs()
                for i, c in enumerate(coeffs):
                    val += c * (alpha ** (deg - i))
                if val != zeros(n, n):
                    h3 = False
                else:
                    vecs = []
                    for i in range(deg):
                        mat = alpha ** i
                        vecs.append(list(mat))
                    M = Matrix(vecs)
                    h3 = bool(M.rank() == deg)
            else:
                h3 = bool(sympy.simplify(p.eval(alpha)) == 0) and bool(p.is_irreducible)
    except Exception:
        h3 = False

    try:
        p = Poly(m, x_sym, domain=F)
        neg_q = not bool(p.is_irreducible)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha is algebraic over F",
    "H_3: m is the minimal polynomial of alpha over F",
    "not Q: The degree of the simple extension is not equal to the degree of m"
]

N_HYP = 3
NEG_Q_INDEX = 3