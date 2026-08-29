import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            m = witness.get('m')
        elif isinstance(witness, (tuple, list)):
            p = witness[0]
            m = witness[1]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: F is a field of characteristic p > 0
    try:
        p = int(p)
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: m(x) in F[x] is the minimal polynomial of alpha over F
    # Any monic polynomial of degree >= 1 is the minimal polynomial of its companion matrix.
    try:
        if isinstance(m, Poly):
            m = m.as_expr()
        m = sympy.sympify(m)
        free_syms = list(m.free_symbols - {x})
        if free_syms:
            domain = sympy.GF(p).frac_field(*free_syms)
        else:
            domain = sympy.GF(p)
        poly_m = Poly(m, x, domain=domain)
        h2 = poly_m.degree() >= 1 and poly_m.is_monic
    except Exception:
        h2 = False

    # neg_Q: m(x) cannot be written as g(x^{p^k}) for any k >= 0 and separable irreducible g(x)
    neg_q = True
    if h1 and h2:
        try:
            deg_m = poly_m.degree()
            max_k = 0
            while p**(max_k + 1) <= deg_m:
                max_k += 1
            
            for k in range(max_k + 1):
                pk = p**k
                monoms = poly_m.monoms()
                # Check if m(x) is a polynomial in x^{p^k}
                if all(deg[0] % pk == 0 for deg in monoms):
                    # Construct g(x) such that m(x) = g(x^{p^k})
                    g_dict = {deg[0] // pk: coeff for deg, coeff in zip(poly_m.monoms(), poly_m.coeffs())}
                    g_poly = Poly.from_dict(g_dict, x, domain=poly_m.domain)
                    
                    # Check if g(x) is irreducible and separable over F
                    if g_poly.is_irreducible:
                        g_deriv = g_poly.diff(x)
                        if not g_deriv.is_zero:
                            neg_q = False
                            break
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic p > 0",
    "H_2: m is the minimal polynomial of alpha over F",
    "¬Q: m cannot be written as g evaluated at x to the p to the k"
]

N_HYP = 2
NEG_Q_INDEX = 2