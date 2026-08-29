import sympy as sp
from sympy.abc import x

def check_H1(witness):
    if not isinstance(witness, (list, tuple, set)):
        witness = [witness]
    try:
        for w in witness:
            sp.Poly(w, x, domain='ZZ')
        return True
    except Exception:
        return False

def analyze_ideal(witness):
    if not isinstance(witness, (list, tuple, set)):
        witness = [witness]
    
    try:
        polys = []
        for w in witness:
            p = sp.Poly(w, x, domain='ZZ')
            if not p.is_zero:
                polys.append(p)
    except Exception:
        return False, False

    if not polys:
        return True, False

    try:
        G = sp.groebner([p.as_expr() for p in polys], x, domain='ZZ')
        G_polys = [sp.Poly(g, x, domain='ZZ') for g in G]
    except Exception:
        return False, False

    constants = [abs(p.LC()) for p in G_polys if p.degree() == 0]
    
    if constants:
        c = constants[0]
        if c == 1:
            return False, False
        if not sp.isprime(c):
            return False, False
            
        try:
            f_mod = sp.Poly(0, x, domain=sp.GF(c))
            for p in G_polys:
                p_mod = sp.Poly(p.as_expr(), x, domain=sp.GF(c))
                if p_mod.is_zero:
                    continue
                if f_mod.is_zero:
                    f_mod = p_mod
                else:
                    f_mod = sp.gcd(f_mod, p_mod)
        except Exception:
            return False, False
            
        if f_mod.is_zero:
            return True, False
        elif f_mod.degree() == 0:
            return False, False
        else:
            is_irred = bool(f_mod.is_irreducible)
            return is_irred, is_irred
    else:
        if len(G_polys) == 1:
            f = G_polys[0]
            if f.content() != 1:
                return False, False
            is_irred = bool(f.is_irreducible)
            return is_irred, False
        else:
            return False, False

def conditions(witness) -> list[bool]:
    H1 = check_H1(witness)
    
    is_domain, is_field = analyze_ideal(witness)
    
    Q = is_domain and not is_field
    neg_Q = not Q
    
    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: witness generates an ideal in Z polynomials",
    "not Q: factor ring is NOT an integral domain OR it IS a field"
]

N_HYP = 1
NEG_Q_INDEX = 1