import sympy
from sympy import Symbol, Poly, Integer, gcd, groebner

x = Symbol('x')

def check_H1(witness):
    if not isinstance(witness, (list, tuple, set)):
        witness = [witness]
    if len(witness) == 0:
        return False
    for w in witness:
        try:
            p = Poly(w, x)
            if not all(isinstance(c, Integer) for c in p.coeffs()):
                return False
        except Exception:
            return False
    return True

def is_isomorphic_to_Z_phi(witness):
    if not isinstance(witness, (list, tuple, set)):
        witness = [witness]
    if len(witness) == 0:
        return False
    polys = []
    for w in witness:
        try:
            p = Poly(w, x)
            if not all(isinstance(c, Integer) for c in p.coeffs()):
                return False
            polys.append(p)
        except Exception:
            return False
    try:
        g_expr = polys[0].as_expr()
        for p in polys[1:]:
            g_expr = gcd(g_expr, p.as_expr())
        g = Poly(g_expr, x)
        cont, prim = g.primitive()
        g = prim
        lc = g.LC()
        if lc == -1:
            g = -g
        elif lc != 1:
            return False
        if g.degree() != 2:
            return False
        coeffs = g.all_coeffs()
        c = coeffs[1]
        d = coeffs[2]
        if c**2 - 4*d != 5:
            return False
        V_exprs = []
        for p in polys:
            q, r = p.div(g)
            V_exprs.append(q.as_expr())
        for v in V_exprs:
            if v == 1 or v == -1:
                return True
        gb = groebner(V_exprs, x, domain='ZZ')
        if len(list(gb)) == 1 and list(gb)[0] == 1:
            return True
    except Exception:
        return False
    return False

def conditions(witness):
    try:
        h1 = check_H1(witness)
    except Exception:
        h1 = False
    try:
        neg_q = not is_isomorphic_to_Z_phi(witness)
    except Exception:
        neg_q = False
    return [h1, neg_q]

CONDITION_LABELS = ["H_1: I is an ideal in Z_x", "not Q: Z_x mod I is not isomorphic to Z_phi"]
N_HYP = 1
NEG_Q_INDEX = 1