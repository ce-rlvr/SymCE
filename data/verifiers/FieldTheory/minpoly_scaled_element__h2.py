import sympy
from sympy import Symbol, Dummy, minimal_polynomial, simplify, sympify
from sympy.abc import x

# Top-level setup
# (No specific named groups or matrices needed for this Field Theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            c = witness.get('c')
            alpha = witness.get('alpha')
            m = witness.get('m')
            n = witness.get('n')
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            c, alpha, m, n = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: F is a field and E/F is a field extension
    try:
        d_x = Dummy('x')
        _ = minimal_polynomial(alpha, d_x)
        h1 = True
    except Exception:
        h1 = False

    # H2: c in F is a non-zero element
    try:
        h2 = bool(c != 0)
    except Exception:
        h2 = False

    # neg_Q: The minimal polynomial of c*alpha over F is NOT c^n * m(x/c)
    try:
        x_sym = Symbol('x')
        minpoly_calpha = minimal_polynomial(c * alpha, x_sym)
        
        if callable(m):
            expected = (c**n * m(x_sym / c)).expand()
        else:
            if hasattr(m, 'as_expr'):
                m_expr = m.as_expr()
            else:
                m_expr = sympify(m)
                
            free_syms = m_expr.free_symbols
            if len(free_syms) == 1:
                sym = list(free_syms)[0]
            elif len(free_syms) == 0:
                sym = Dummy('sym')
            else:
                if x_sym in free_syms:
                    sym = x_sym
                else:
                    sym = list(free_syms)[0]
                    
            expected = (c**n * m_expr.subs(sym, x_sym / c)).expand()
        
        diff = simplify(minpoly_calpha - expected)
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field and E/F is a field extension",
    "H_2: c in F is a non-zero element",
    "¬Q: The minimal polynomial of c*alpha over F is not c^n * m(x/c)"
]

N_HYP = 2
NEG_Q_INDEX = 2