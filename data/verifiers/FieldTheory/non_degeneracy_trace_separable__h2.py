import sympy
from sympy.abc import x, t

def conditions(witness) -> list[bool]:
    try:
        expr, p = witness
        expr = sympy.sympify(expr)
        p = int(p)
        poly = sympy.Poly(expr, x, t, domain=sympy.GF(p))
        h1 = bool(poly.is_irreducible)
    except Exception:
        h1 = False

    try:
        expr, p = witness
        expr = sympy.sympify(expr)
        p = int(p)
        poly_x = sympy.Poly(expr, x)
        n = poly_x.degree()
        coeffs = poly_x.all_coeffs()
        
        C = sympy.zeros(n, n)
        for i in range(n - 1):
            C[i + 1, i] = 1
        for i in range(n):
            C[i, n - 1] = -coeffs[n - i]
            
        traces = []
        Ck = sympy.eye(n)
        for _ in range(2 * n - 1):
            traces.append(sympy.trace(Ck))
            Ck = Ck * C
            
        M = sympy.zeros(n, n)
        for i in range(n):
            for j in range(n):
                M[i, j] = traces[i + j]
                
        det_M = M.det()
        det_poly = sympy.Poly(sympy.expand(det_M), t, domain=sympy.GF(p))
        neg_q = bool(det_poly.is_zero)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite field extension",
    "¬Q: The trace pairing is degenerate"
]

N_HYP = 1
NEG_Q_INDEX = 1