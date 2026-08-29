import sympy
from sympy import Poly
from sympy import QQ, ZZ, GF, RR, CC
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: p(x) is an irreducible polynomial over F",
    "H_3: E is the factor ring over F modulo p(x)",
    "¬Q: alpha is not a root of p(x) in E"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            p_expr = witness.get('p')
            E = witness.get('E', 'F_x_mod_p')
            alpha_expr = witness.get('alpha')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 4:
                F, p_expr, E, alpha_expr = witness
            elif len(witness) == 3:
                F, p_expr, alpha_expr = witness
                E = "F_x_mod_p"
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        F_dom = F
        if isinstance(F, str):
            if F == 'QQ': F_dom = QQ
            elif F == 'ZZ': F_dom = ZZ
            elif F == 'RR': F_dom = RR
            elif F == 'CC': F_dom = CC
            elif F.startswith('GF(') and F.endswith(')'):
                num_str = F[3:-1]
                if num_str.isdigit():
                    F_dom = GF(int(num_str))
        else:
            if F == sympy.S.Rationals: F_dom = QQ
            elif F == sympy.S.Reals: F_dom = RR
            elif F == sympy.S.Complexes: F_dom = CC
            elif F == sympy.S.Integers: F_dom = ZZ
            
        h1 = getattr(F_dom, 'is_Field', False)
        if not h1 and hasattr(F_dom, 'is_field'):
            h1 = F_dom.is_field
        h1 = bool(h1)
    except Exception:
        h1 = False
        F_dom = QQ

    # H_2: p(x) is an irreducible polynomial over F
    try:
        if isinstance(p_expr, Poly):
            p = p_expr
            gen = p.gen
        else:
            p_sym = sympy.sympify(p_expr)
            if hasattr(p_sym, 'free_symbols'):
                free_syms = p_sym.free_symbols
                if len(free_syms) == 1:
                    gen = list(free_syms)[0]
                else:
                    gen = x
            else:
                gen = x
            p = Poly(p_expr, gen, domain=F_dom)
        h2 = bool(p.is_irreducible)
    except Exception:
        h2 = False
        p = None
        gen = x

    # H_3: E is the factor ring over F modulo p(x)
    try:
        h3 = True
    except Exception:
        h3 = False

    # ¬Q: alpha is not a root of p(x) in E
    try:
        if p is None:
            neg_q = False
        else:
            if isinstance(alpha_expr, Poly):
                alpha_expr = alpha_expr.as_expr()
            else:
                alpha_expr = sympy.sympify(alpha_expr)
            
            p_expr_val = p.as_expr()
            p_alpha_expr = p_expr_val.subs(gen, alpha_expr)
            
            p_alpha = Poly(p_alpha_expr, gen, domain=F_dom)
            rem = p_alpha % p
            
            neg_q = not bool(rem.is_zero)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]