import sympy
from sympy import QQ, GF, Poly, Symbol, sqrt, I
from sympy.abc import x

# Top-level setup
Q = QQ
F2 = GF(2)
F3 = GF(3)
F5 = GF(5)
F7 = GF(7)

def conditions(witness):
    try:
        F, K, alpha, m, L = witness
    except Exception:
        return [False, False, False, False]
        
    def is_subfield(sub, sup):
        if not (hasattr(sub, 'is_Field') and sub.is_Field): return False
        if not (hasattr(sup, 'is_Field') and sup.is_Field): return False
        if sub == sup: return True
        if sub == sympy.QQ: return sup.char == 0
        if sub.char != sup.char: return False
        
        if sub.char == 0:
            try:
                if hasattr(sub, 'ext'):
                    for gen in sub.ext.args:
                        sup.from_expr(gen)
                    return True
            except Exception:
                pass
            try:
                if hasattr(sub, 'orig_ext'):
                    exts = sub.orig_ext if isinstance(sub.orig_ext, tuple) else (sub.orig_ext,)
                    for gen in exts:
                        sup.from_expr(gen)
                    return True
            except Exception:
                pass
        else:
            if hasattr(sub, 'order') and sub.order == sub.char:
                return True
        return False

    def is_in_field(expr, field):
        try:
            field.from_expr(expr)
            return True
        except Exception:
            return False

    try:
        h1 = is_subfield(F, K)
    except Exception:
        h1 = False

    try:
        h2 = is_in_field(alpha, K)
    except Exception:
        h2 = False

    try:
        if not isinstance(m, sympy.Poly):
            m_poly = sympy.Poly(m, x)
        else:
            m_poly = m

        if m_poly.LC() != 1:
            h3 = False
        else:
            coeffs_in_F = True
            for c in m_poly.coeffs():
                try:
                    F.from_expr(c)
                except Exception:
                    coeffs_in_F = False
                    break
            
            if not coeffs_in_F:
                h3 = False
            else:
                val = m_poly.eval(alpha)
                if hasattr(val, 'simplify'):
                    val = val.simplify()
                
                is_root = False
                if val == 0:
                    is_root = True
                else:
                    try:
                        if int(val) == 0:
                            is_root = True
                    except Exception:
                        pass
                
                if not is_root:
                    h3 = False
                else:
                    m_F = sympy.Poly(m_poly, domain=F)
                    factors = m_F.factor_list()
                    if len(factors[1]) != 1 or factors[1][0][1] != 1:
                        h3 = False
                    else:
                        h3 = True
    except Exception:
        h3 = False

    try:
        if L.char == 0:
            roots_dict = sympy.roots(m_poly)
            num_roots = 0
            for r in roots_dict:
                try:
                    L.from_expr(r)
                    num_roots += 1
                except Exception:
                    pass
        else:
            m_L = sympy.Poly(m_poly, domain=L)
            roots_dict = m_L.ground_roots()
            num_roots = len(roots_dict)
            
        if is_subfield(F, L):
            num_homs = num_roots
        else:
            num_homs = 0
            
        neg_q = (num_homs != num_roots)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a subfield of K",
    "H_2: alpha in K is algebraic over F",
    "H_3: m is the minimal polynomial of alpha over F",
    "not Q: number of F-homs to L != number of roots of m in L"
]

N_HYP = 3
NEG_Q_INDEX = 3