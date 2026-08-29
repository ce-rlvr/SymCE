import sympy
from sympy import Poly
from sympy.abc import x, y, z

# Top-level setup
# (No specific named objects required for this ring theory conjecture, 
# but we provide standard variables for convenience)

def conditions(witness) -> list[bool]:
    """
    Check the hypotheses and negated conclusion for the false conjecture:
    'Primitive Factors of Primitive Polynomials in a UFD' (where UFD hypothesis is dropped).
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                f_expr, g_expr, var = witness
                f = Poly(f_expr, var)
                g = Poly(g_expr, var)
            elif len(witness) == 2:
                f, g = witness
            else:
                return [False, False, False, False]
        else:
            f = witness.f
            g = witness.g
    except Exception:
        return [False, False, False, False]

    # Attempt to convert to Poly if they are expressions
    try:
        if not isinstance(f, Poly) and hasattr(f, 'free_symbols'):
            syms = list(f.free_symbols)
            if len(syms) == 1:
                f = Poly(f, syms[0])
        if not isinstance(g, Poly) and hasattr(g, 'free_symbols'):
            syms = list(g.free_symbols)
            if len(syms) == 1:
                g = Poly(g, syms[0])
    except Exception:
        pass

    def is_prim(p):
        if hasattr(p, 'is_primitive'):
            val = p.is_primitive
            if callable(val): return val()
            if val is not None: return val
        if hasattr(p, 'content'):
            c = p.content()
            if hasattr(c, 'is_unit'):
                val = c.is_unit
                if callable(val): return val()
                if val is not None: return val
            return c == 1 or c == -1
        return False

    def is_irred(p):
        if hasattr(p, 'is_irreducible'):
            val = p.is_irreducible
            if callable(val): return val()
            if val is not None: return val
        return False

    def divides(p1, p2):
        if hasattr(p1, 'divides'):
            try:
                val = p1.divides(p2)
                if val is not None: return val
            except Exception:
                pass
        if hasattr(p2, 'rem'):
            try:
                r = p2.rem(p1)
                if hasattr(r, 'is_zero'):
                    return r.is_zero
                return r == 0
            except Exception:
                pass
        try:
            return (p2 % p1) == 0
        except Exception:
            return False

    try:
        h1 = bool(is_prim(f))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_irred(g))
    except Exception:
        h2 = False

    try:
        h3 = bool(divides(g, f))
    except Exception:
        h3 = False

    try:
        neg_q = not bool(is_prim(g))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a primitive polynomial",
    "H_2: g is an irreducible polynomial",
    "H_3: g divides f",
    "¬Q: g is not primitive"
]

N_HYP = 3
NEG_Q_INDEX = 3