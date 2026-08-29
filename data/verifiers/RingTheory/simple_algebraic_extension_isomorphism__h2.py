import sympy
from sympy import Poly, Symbol, QQ, ZZ

# Top-level setup for witness expressions
x = Symbol('x')
t = Symbol('t')

def conditions(witness):
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            E = witness.get('E')
            alpha = witness.get('alpha')
            m = witness.get('m')
            x_sym = witness.get('x', x)
        else:
            F, E, alpha, m, x_sym = witness
    except Exception:
        return [False, False, False]

    # H_1: E is an extension field of F
    try:
        h1 = False
        valid_fields = (sympy.QQ, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes)
        if F in valid_fields and E in valid_fields:
            h1 = True
        elif hasattr(F, 'is_Field') and hasattr(E, 'is_Field') and F.is_Field and E.is_Field:
            h1 = True
        elif F in valid_fields and getattr(E, 'is_Field', False):
            h1 = True
    except Exception:
        h1 = False

    # H_2: m(x) is the minimal polynomial of alpha over F
    try:
        h2 = False
        if not isinstance(m, sympy.Poly):
            m_poly = sympy.Poly(m, x_sym)
        else:
            m_poly = m
        
        if m_poly.gen == x_sym:
            coeffs_in_F = True
            if F in (sympy.QQ, sympy.S.Rationals):
                for c in m_poly.coeffs():
                    if not getattr(c, 'is_rational', True):
                        coeffs_in_F = False
                        break
            elif F == sympy.S.Reals:
                for c in m_poly.coeffs():
                    if not getattr(c, 'is_real', True):
                        coeffs_in_F = False
                        break
            elif hasattr(F, 'of_type'):
                for c in m_poly.coeffs():
                    if not F.of_type(c):
                        try:
                            F.convert(c)
                        except Exception:
                            coeffs_in_F = False
                            break
            
            if coeffs_in_F:
                if m_poly.is_zero:
                    is_val_zero = True
                else:
                    try:
                        val = m_poly.as_expr().subs(x_sym, alpha)
                        if hasattr(val, 'simplify'):
                            val = sympy.simplify(val)
                        is_val_zero = (val == 0) or (getattr(val, 'is_zero', False) is True)
                    except Exception:
                        try:
                            val = m_poly.eval(alpha)
                            is_val_zero = (val == 0)
                        except Exception:
                            is_val_zero = False
                
                if is_val_zero:
                    if m_poly.is_zero:
                        is_transcendental = False
                        if hasattr(alpha, 'free_symbols') and alpha.free_symbols:
                            is_transcendental = True
                        elif hasattr(alpha, 'is_number') and not alpha.is_number:
                            is_transcendental = True
                        elif type(alpha).__name__ in ('FracElement', 'PolyElement'):
                            is_transcendental = True
                        elif alpha in (sympy.pi, sympy.E):
                            is_transcendental = True
                        
                        if is_transcendental:
                            h2 = True
                    else:
                        if m_poly.is_monic and m_poly.is_irreducible:
                            h2 = True
    except Exception:
        h2 = False

    # neg_Q: The factor ring modulo m(x) is NOT isomorphic to the simple extension field F(alpha)
    try:
        neg_q = False
        if not isinstance(m, sympy.Poly):
            m_poly_q = sympy.Poly(m, x_sym)
        else:
            m_poly_q = m
            
        if m_poly_q.is_zero:
            neg_q = True
        elif not m_poly_q.is_irreducible:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is an extension field of F",
    "H_2: m(x) is the minimal polynomial of alpha over F",
    "not Q: The factor ring modulo m(x) is NOT isomorphic to the simple extension field F(alpha)"
]

N_HYP = 2
NEG_Q_INDEX = 2