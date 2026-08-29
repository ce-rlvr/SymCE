import sympy
from sympy import QQ, Poly, simplify, minpoly, sympify, roots
from sympy.abc import x

# Top-level setup
# (No special groups or matrices needed for this field theory conjecture)

def extract_witness(witness):
    if isinstance(witness, dict):
        return witness.get('F'), witness.get('E'), witness.get('alpha'), witness.get('m')
    elif isinstance(witness, (tuple, list)):
        if len(witness) >= 4:
            return witness[0], witness[1], witness[2], witness[3]
    return getattr(witness, 'F', None), getattr(witness, 'E', None), getattr(witness, 'alpha', None), getattr(witness, 'm', None)

def conditions(witness) -> list[bool]:
    F, E, alpha, m = extract_witness(witness)
    
    # H1: F is a field
    try:
        h1 = False
        if hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif hasattr(F, 'is_field') and F.is_field:
            h1 = True
        elif F == QQ:
            h1 = True
    except Exception:
        h1 = False

    # H2: E is a finite Galois extension of F
    try:
        h2 = False
        if E == F:
            h2 = True
        elif hasattr(E, 'domain') and E.domain == F:
            # Check if E is Galois over F
            if hasattr(E, 'ext') and hasattr(E.ext, 'minpoly'):
                minpoly_E = E.ext.minpoly
                rts = roots(minpoly_E.as_expr())
                if sum(rts.values()) == minpoly_E.degree():
                    h2 = True
                    for r in rts:
                        try:
                            E.from_sympy(r)
                        except Exception:
                            h2 = False
                            break
    except Exception:
        h2 = False

    # H3: alpha in E is an element algebraic over F
    try:
        h3 = False
        if hasattr(alpha, 'as_expr'):
            alpha_expr = alpha.as_expr()
        else:
            alpha_expr = sympify(alpha)
            
        if E == F:
            # alpha must be in F
            if alpha_expr.is_Rational and F == QQ:
                h3 = True
            elif hasattr(F, 'from_sympy'):
                try:
                    F.from_sympy(alpha_expr)
                    h3 = True
                except Exception:
                    pass
        elif h2:
            try:
                E.from_sympy(alpha_expr)
                h3 = True
            except Exception:
                pass
    except Exception:
        h3 = False

    # neg_Q: m(x) != ∏_{β ∈ S} (x - β)
    try:
        neg_q = False
        if m is not None:
            if hasattr(alpha, 'as_expr'):
                alpha_expr = alpha.as_expr()
            else:
                alpha_expr = sympify(alpha)
                
            # The product of (x - beta) over Galois conjugates is the minimal polynomial of alpha over F
            try:
                if F == QQ:
                    mp = minpoly(alpha_expr, x)
                else:
                    mp = minpoly(alpha_expr, x, domain=F)
            except Exception:
                mp = None
                
            if mp is not None:
                if callable(m):
                    m_expr = m(x)
                elif isinstance(m, str):
                    m_expr = sympify(m)
                elif isinstance(m, Poly):
                    m_expr = m.as_expr()
                else:
                    m_expr = sympify(m)
                    
                free_syms = m_expr.free_symbols
                if len(free_syms) == 1:
                    sym = list(free_syms)[0]
                    m_expr = m_expr.subs(sym, x)
                    
                diff = simplify(m_expr - mp)
                neg_q = (diff != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is a finite Galois extension of F",
    "H_3: α ∈ E is an element algebraic over F",
    "¬Q: m(x) is not the product of (x - β) over the Galois conjugates of α"
]

N_HYP = 3
NEG_Q_INDEX = 3