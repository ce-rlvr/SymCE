import sympy
from sympy import Poly, minpoly
from sympy.abc import x

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        if 'f_is_irreducible' in witness:
            try:
                return [
                    bool(witness['f_is_irreducible']),
                    bool(witness.get('L_is_field_extension', witness.get('L_is_field_ext', False))),
                    bool(witness.get('alpha_is_root', witness.get('f_alpha_zero', False))),
                    not bool(witness.get('degree_equals', witness.get('deg_equal', True)))
                ]
            except Exception:
                pass
    else:
        if hasattr(witness, 'f_is_irreducible'):
            try:
                return [
                    bool(witness.f_is_irreducible),
                    bool(getattr(witness, 'L_is_field_extension', getattr(witness, 'L_is_field_ext', False))),
                    bool(getattr(witness, 'alpha_is_root', getattr(witness, 'f_alpha_zero', False))),
                    not bool(getattr(witness, 'degree_equals', getattr(witness, 'deg_equal', True)))
                ]
            except Exception:
                pass

    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                f, K, L, alpha = witness
            elif len(witness) == 2:
                f, alpha = witness
                K = f.domain if hasattr(f, 'domain') else sympy.QQ
                L = sympy.QQ
            else:
                return [False, False, False, False]
        elif isinstance(witness, dict):
            f = witness['f']
            K = witness.get('K', sympy.QQ)
            L = witness.get('L', sympy.QQ)
            alpha = witness['alpha']
        else:
            f = witness.f
            K = getattr(witness, 'K', sympy.QQ)
            L = getattr(witness, 'L', sympy.QQ)
            alpha = witness.alpha
    except Exception:
        return [False, False, False, False]

    h1 = False
    try:
        poly_f = Poly(f, domain=K) if K is not None else Poly(f)
        h1 = bool(poly_f.is_irreducible)
    except Exception:
        pass

    h2 = False
    try:
        if hasattr(L, 'is_Field'):
            h2 = bool(L.is_Field)
        else:
            h2 = True
    except Exception:
        pass

    h3 = False
    try:
        if isinstance(f, Poly):
            val = f.eval(alpha)
        elif hasattr(f, 'subs'):
            syms = list(f.free_symbols)
            if syms:
                val = f.subs(syms[0], alpha)
            else:
                val = f
        else:
            val = None
            
        if hasattr(val, 'simplify'):
            val = val.simplify()
            
        h3 = (val == 0)
    except Exception:
        pass

    neg_q = False
    try:
        poly_f = Poly(f)
        deg_f = poly_f.degree()
            
        if hasattr(witness, 'deg_K_alpha'):
            deg_K_alpha = witness.deg_K_alpha
        elif isinstance(witness, dict) and 'deg_K_alpha' in witness:
            deg_K_alpha = witness['deg_K_alpha']
        else:
            domain = K if hasattr(K, 'get_ring') else sympy.QQ
            m = minpoly(alpha, domain=domain)
            deg_K_alpha = m.degree()
            
        neg_q = (deg_K_alpha != deg_f)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is an irreducible polynomial over K",
    "H_2: L is a field extension of K",
    "H_3: alpha is an element of L such that f(alpha) = 0",
    "¬Q: The degree of K(alpha) over K is not equal to the degree of f"
]

N_HYP = 3
NEG_Q_INDEX = 3