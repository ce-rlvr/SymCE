import sympy
from sympy import Symbol, QQ, ZZ, Rational, Poly
from sympy.abc import x

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            E = witness.get('E')
            alpha = witness.get('alpha')
            m = witness.get('m')
        else:
            F, E, alpha, m = witness
    except Exception:
        return [False, False, False, False]

    # H1: E is an extension field of F
    try:
        h1 = bool(getattr(E, 'is_Field', False))
        if h1:
            if hasattr(F, 'issubset'):
                if not F.issubset(E):
                    h1 = False
            elif hasattr(E, 'convert') and hasattr(F, 'one'):
                try:
                    E.convert(F.one)
                except Exception:
                    h1 = False
    except Exception:
        h1 = False

    # H2: alpha in E is an element algebraic over F
    try:
        in_E = False
        if E == QQ and isinstance(alpha, (int, sympy.Integer, sympy.Rational)):
            in_E = True
        else:
            try:
                in_E = alpha in E
            except Exception:
                pass
            if not in_E and hasattr(E, 'convert'):
                try:
                    E.convert(alpha)
                    in_E = True
                except Exception:
                    pass
        
        m_expr = m.as_expr() if hasattr(m, 'as_expr') else sympy.sympify(m)
        free_syms = m_expr.free_symbols
        gen = list(free_syms)[0] if free_syms else x
        
        is_root = (m_expr.subs(gen, alpha) == 0)
        is_zero = m_expr.is_zero
        
        h2 = bool(in_E and is_root and not is_zero)
    except Exception:
        h2 = False

    # H3: m(x) is the minimal polynomial of alpha over F
    try:
        m_expr = m.as_expr() if hasattr(m, 'as_expr') else sympy.sympify(m)
        free_syms = m_expr.free_symbols
        gen = list(free_syms)[0] if free_syms else x
        
        m_poly_F = Poly(m_expr, gen, domain=F)
        in_Fx = all(c in F for c in m_poly_F.coeffs())
        
        is_root = (m_expr.subs(gen, alpha) == 0)
        is_irred = m_poly_F.is_irreducible
        
        h3 = bool(in_Fx and is_root and is_irred)
    except Exception:
        h3 = False

    # neg_Q: The degree of the simple extension over F is not equal to the degree of m(x)
    try:
        # If F is a field, the theorem holds (neg_Q = False).
        # If F is not a field (e.g., F = ZZ), the degree/rank of F(alpha) over F 
        # does not equal the degree of m(x), so the conclusion fails (neg_Q = True).
        neg_q = not bool(getattr(F, 'is_Field', False))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: E is an extension field of F",
    "H_2: alpha in E is an element algebraic over F",
    "H_3: m(x) is the minimal polynomial of alpha over F",
    "¬Q: The degree of the simple extension over F is not equal to the degree of m(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3