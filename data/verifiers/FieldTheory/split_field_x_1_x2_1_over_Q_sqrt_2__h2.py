import sympy
from sympy import sqrt, I, Symbol
from sympy.polys.numberfields import primitive_element

# Top-level setup for witness expressions
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a polynomial f(x), or a tuple (F_gens, f(x), K_gens).
    """
    # Parse witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F_gens, f, K_gens = witness
            elif len(witness) == 2:
                f, K_gens = witness
                F_gens = [sqrt(2)]
            else:
                return [False, False, False]
        else:
            f = witness
            F_gens = [sqrt(2)]
            K_gens = None
            
        f_expr = sympy.sympify(f)
        free_syms = f_expr.free_symbols
        var = list(free_syms)[0] if len(free_syms) == 1 else x
        rts = sympy.roots(f_expr, var)
        
        if K_gens is None:
            K_gens = F_gens + list(rts.keys())
    except Exception:
        return [False, False, False]

    def field_degree(gens):
        clean_gens = []
        for g in gens:
            g_sym = sympy.sympify(g)
            if not g_sym.is_rational and g_sym not in clean_gens:
                clean_gens.append(g_sym)
        if not clean_gens:
            return 1
        dummy = Symbol('dummy')
        minpoly, _ = primitive_element(clean_gens, x=dummy, ex=True)
        return sympy.degree(minpoly, dummy)

    def in_field(elem, gens):
        if sympy.sympify(elem).is_rational:
            return True
        try:
            deg_base = field_degree(gens)
            deg_ext = field_degree(gens + [elem])
            return deg_base == deg_ext
        except Exception:
            return False

    # H1: F = Q(sqrt(2))
    try:
        deg_F = field_degree(F_gens)
        h1_ok = bool((deg_F == 2) and in_field(sqrt(2), F_gens))
    except Exception:
        h1_ok = False

    # H2: K is the splitting field of f over F
    try:
        f_poly = sympy.Poly(f_expr, var)
        
        if f_poly.degree() < 1:
            h2_ok = False
        else:
            all_roots_found = (sum(rts.values()) == f_poly.degree())
            
            k_contains_f = all(in_field(g, K_gens) for g in F_gens)
            k_contains_roots = all(in_field(r, K_gens) for r in rts.keys())
            
            deg_K = field_degree(K_gens)
            deg_split = field_degree(F_gens + list(rts.keys()))
            k_is_minimal = (deg_K == deg_split)
            
            h2_ok = bool(all_roots_found and k_contains_f and k_contains_roots and k_is_minimal)
    except Exception:
        h2_ok = False

    # neg_Q: not (K == Q(sqrt(2), i) and [K:F] == 2)
    try:
        deg_K = field_degree(K_gens)
        deg_F = field_degree(F_gens)
        
        is_K_target = bool((deg_K == 4) and in_field(sqrt(2), K_gens) and in_field(I, K_gens))
        is_deg_2 = bool(deg_K == 2 * deg_F)
        
        q_ok = is_K_target and is_deg_2
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F = Q(sqrt(2))",
    "H_2: K is the splitting field of f(x) over F",
    "¬Q: K != Q(sqrt(2), i) or degree of K over F != 2"
]

N_HYP = 2
NEG_Q_INDEX = 2