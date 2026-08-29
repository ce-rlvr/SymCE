import sympy
from sympy.abc import x

# Top-level setup
# (No additional bindings needed for this domain)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    sym = x
    n_val = -1
    
    try:
        if isinstance(witness, int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            n = int(witness)
            if n >= 0:
                n_val = n
                h1 = True
        else:
            f_expr = sympy.sympify(witness)
            symbols = f_expr.free_symbols
            if len(symbols) == 1:
                sym = list(symbols)[0]
            poly_f = sympy.Poly(f_expr, sym)
            n = poly_f.degree()
            if n >= 0:
                expected_f = sum((sym**i)/sympy.factorial(i) for i in range(n + 1))
                if sympy.simplify(f_expr - expected_f) == 0:
                    n_val = n
                    h1 = True
    except Exception:
        h1 = False

    try:
        if h1 and n_val >= 0:
            exact_f = sum((sym**i)/sympy.factorial(i) for i in range(n_val + 1))
            poly_f = sympy.Poly(exact_f, sym, domain='QQ')
            # A polynomial of degree 0 (like 1) is a unit, hence not irreducible.
            if poly_f.degree() <= 0:
                is_irred = False
            else:
                is_irred = poly_f.is_irreducible
            neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is the n-th truncated exponential polynomial",
    "¬Q: f(x) is not irreducible over Q"
]

N_HYP = 1
NEG_Q_INDEX = 1