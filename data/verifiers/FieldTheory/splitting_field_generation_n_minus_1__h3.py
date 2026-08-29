import sympy
from sympy import QQ, Symbol, prod, expand, simplify, sympify, Poly

# Top-level setup
x = Symbol('x')

def get_field(gens):
    valid_gens = []
    for g in gens:
        g_sym = sympify(g)
        if not g_sym.is_Rational and g_sym not in valid_gens:
            valid_gens.append(g_sym)
    if not valid_gens:
        return QQ
    return QQ.algebraic_field(*valid_gens)

def in_field(expr, field):
    try:
        field.from_sympy(sympify(expr))
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    F_gens = list(witness.get('F_gens', []))
    E_gens = list(witness.get('E_gens', []))
    roots = list(witness.get('roots', []))
    f_expr = witness.get('f', x)
    
    # H1: F is a field
    try:
        F_field = get_field(F_gens)
        E_field = get_field(E_gens)
        h1 = True
    except Exception:
        h1 = False
        F_field = None
        E_field = None

    p = None
    # H2: f(x) is a polynomial in F[x] of degree n
    try:
        f = sympify(f_expr)
        roots = [sympify(r) for r in roots]
        n = len(roots)
        p = Poly(f, x)
        h2 = (p.degree() == n)
        if h2 and F_field is not None:
            for c in p.coeffs():
                if not in_field(c, F_field):
                    h2 = False
                    break
        elif F_field is None:
            h2 = False
    except Exception:
        h2 = False

    # H3: alpha_1 to alpha_n are the roots of f(x) in E such that f(x) = c(x-alpha_1)...(x-alpha_n)
    try:
        if F_field is not None and E_field is not None and p is not None:
            c = p.LC()
            h3 = in_field(c, F_field)
            if h3:
                for r in roots:
                    if not in_field(r, E_field):
                        h3 = False
                        break
            if h3:
                expected_f = c * prod(x - r for r in roots)
                diff = expand(f - expected_f)
                if diff != 0:
                    diff = simplify(diff)
                if diff != 0:
                    h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: E != F(alpha_1 to alpha_{n-1})
    try:
        if F_field is not None and E_field is not None:
            F_alpha_gens = F_gens + roots[:-1]
            F_alpha_field = get_field(F_alpha_gens)
            
            E_in_F_alpha = all(in_field(g, F_alpha_field) for g in E_gens)
            F_alpha_in_E = all(in_field(g, E_field) for g in F_alpha_gens)
            
            E_equals_F_alpha = E_in_F_alpha and F_alpha_in_E
            neg_q = not E_equals_F_alpha
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial in F of degree n",
    "H_3: all n roots of f are in E and f splits in E",
    "¬Q: E is not generated over F by the first n minus 1 roots"
]

N_HYP = 3
NEG_Q_INDEX = 3