import sympy
from sympy import Poly
from sympy.abc import x

def is_real_gen(g):
    try:
        if getattr(g, 'is_real', None) is not None:
            return bool(g.is_real)
    except Exception:
        pass
    try:
        if hasattr(g, 'ext'):
            return is_real_gen(g.ext)
    except Exception:
        pass
    try:
        c = complex(g)
        return c.imag == 0
    except Exception:
        pass
    try:
        v = g.evalf()
        if getattr(v, 'is_real', None) is not None:
            return bool(v.is_real)
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f, K = witness
        else:
            f = witness
            K = None
    except Exception:
        f = witness
        K = None

    # H_1: f in Q[x] is an irreducible polynomial of degree 3
    h1 = False
    try:
        if isinstance(f, Poly):
            poly_h1 = f.set_domain('QQ')
        else:
            syms = getattr(f, "free_symbols", set())
            if len(syms) != 1:
                raise ValueError
            sym = list(syms)[0]
            poly_h1 = Poly(f, sym, domain='QQ')
        
        if poly_h1.degree() == 3:
            h1 = poly_h1.is_irreducible
    except Exception:
        h1 = False

    # H_2: All three roots of f in C are real numbers
    h2 = False
    try:
        if isinstance(f, Poly):
            poly_h2 = f
        else:
            syms = getattr(f, "free_symbols", set())
            if len(syms) != 1:
                raise ValueError
            sym = list(syms)[0]
            poly_h2 = Poly(f, sym)
            
        if poly_h2.degree() == 3:
            coeffs_real = True
            for c in poly_h2.coeffs():
                if getattr(c, 'is_real', None) is False:
                    coeffs_real = False
                    break
                try:
                    if complex(c).imag != 0:
                        coeffs_real = False
                        break
                except Exception:
                    pass
            
            if coeffs_real:
                try:
                    h2 = bool(poly_h2.discriminant() >= 0)
                except Exception:
                    h2 = False
            else:
                roots = sympy.roots(poly_h2, cubics=True)
                if sum(roots.values()) == 3:
                    h2 = all(is_real_gen(r) for r in roots.keys())
    except Exception:
        h2 = False

    # neg_Q: K is a subfield of the real numbers R
    neg_q = False
    try:
        if K is None:
            # If K is not explicitly provided, we assume K is the splitting field of f.
            # The splitting field of a cubic is real iff all its roots are real.
            neg_q = h2
        else:
            if isinstance(K, (list, tuple, set)):
                neg_q = all(is_real_gen(g) for g in K)
            else:
                neg_q = is_real_gen(K)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is an irreducible polynomial of degree 3 over Q",
    "H_2: All three roots of f are real numbers",
    "neg_Q: K is a subfield of R"
]

N_HYP = 2
NEG_Q_INDEX = 2