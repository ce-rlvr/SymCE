import sympy
from sympy import Poly, factor, Symbol, Expr, minpoly, QQ, ZZ, RR, CC, I
from sympy.abc import x

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide F, alpha, p, and t.
    """
    # Extract witness
    if isinstance(witness, dict):
        F = witness.get('F', sympy.QQ)
        alpha = witness.get('alpha')
        p = witness.get('p')
        t = witness.get('t')
    else:
        try:
            F, alpha, p, t = witness
        except Exception:
            return [False, False, False, False]

    # H1: F is a field
    try:
        if isinstance(F, str):
            if F == 'QQ': F = sympy.QQ
            elif F == 'RR': F = sympy.RR
            elif F == 'CC': F = sympy.CC
            elif F == 'ZZ': F = sympy.ZZ
        
        h1 = getattr(F, 'is_Field', False)
        if not h1 and F in [sympy.QQ, sympy.RR, sympy.CC]:
            h1 = True
    except Exception:
        h1 = False

    # H2: alpha is an algebraic element over F
    try:
        alpha_sym = sympy.sympify(alpha)
        mp = sympy.minpoly(alpha_sym)
        h2 = mp is not None and mp.degree() > 0
    except Exception:
        h2 = False

    # H3: p in F[x] is the minimal polynomial of alpha over F
    try:
        alpha_sym = sympy.sympify(alpha)
        p_expr = sympy.sympify(p)
        
        free_symbols = p_expr.free_symbols
        gen = sympy.Symbol('x')
        for s in free_symbols:
            if str(s) == 'x':
                gen = s
        if not free_symbols:
            gen = sympy.Symbol('x')
            
        p_poly = sympy.Poly(p_expr, gen)
        
        is_monic = p_poly.LC() == 1
        val = p_poly.eval(alpha_sym)
        is_root = sympy.simplify(val) == 0
        is_irred = p_poly.is_irreducible
            
        h3 = bool(is_monic and is_root and is_irred)
    except Exception:
        h3 = False

    # Neg_Q: p is NOT the minimal polynomial of alpha over F(t)
    try:
        t_sym = sympy.sympify(t)
        p_expr = sympy.sympify(p)
        
        free_symbols = p_expr.free_symbols
        gen = sympy.Symbol('x')
        for s in free_symbols:
            if str(s) == 'x':
                gen = s
        if not free_symbols:
            gen = sympy.Symbol('x')
                
        if t_sym.is_Symbol:
            p_poly_t = sympy.Poly(p_expr, gen, domain=sympy.QQ.frac_field(t_sym))
            is_irred = p_poly_t.is_irreducible
        else:
            factored_p_t = sympy.factor(p_expr, extension=t_sym)
            if factored_p_t.is_Mul:
                x_factors = [arg for arg in factored_p_t.args if arg.has(gen)]
                has_pow = any(arg.is_Pow and arg.has(gen) for arg in x_factors)
                is_irred = not (len(x_factors) > 1 or has_pow)
            elif factored_p_t.is_Pow and factored_p_t.has(gen):
                is_irred = False
            else:
                is_irred = True
                
        neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha is an algebraic element over F",
    "H_3: p is the minimal polynomial of alpha over F",
    "neg_Q: p is not the minimal polynomial of alpha over F(t)"
]

N_HYP = 3
NEG_Q_INDEX = 3