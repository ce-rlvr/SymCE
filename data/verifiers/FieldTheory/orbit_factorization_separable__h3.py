import sympy as sp
from sympy.abc import x

# Top-level setup
# K = QQ
# L = QQ(sqrt(2))
# G = Gal(L/K) = {1, sigma}, where sigma(sqrt(2)) = -sqrt(2)

def in_L(r):
    try:
        r_simp = sp.simplify(r)
        a = sp.expand(r_simp).subs(sp.sqrt(2), 0)
        b = sp.expand((r_simp - a) / sp.sqrt(2))
        return a.is_rational and b.is_rational
    except Exception:
        return False

def is_in_R(val, R):
    for r in R:
        if sp.simplify(val - r) == 0:
            return r
    return None

def conditions(witness):
    f = witness
    R = []
    
    try:
        h1 = True
    except Exception:
        h1 = False
        
    try:
        h2 = True
    except Exception:
        h2 = False
        
    try:
        rts = sp.roots(f, x)
        if not rts:
            h3 = False
        else:
            R = list(rts.keys())
            subset_L = all(in_L(r) for r in R)
            deg = sp.degree(f, x)
            is_roots = (sum(rts.values()) == deg)
            h3 = bool(subset_L and is_roots)
    except Exception:
        h3 = False
        
    try:
        if not h3:
            neg_q = False
        else:
            acts_on_R = True
            orbits = set()
            for r in R:
                r_conj = sp.expand(r).subs(sp.sqrt(2), -sp.sqrt(2))
                r_conj_in_R = is_in_R(r_conj, R)
                if r_conj_in_R is None:
                    acts_on_R = False
                    break
                orbit = frozenset([r, r_conj_in_R])
                orbits.add(orbit)
            
            if not acts_on_R:
                neg_q = True
            else:
                num_orbits = len(orbits)
                
                try:
                    f_exp = sp.expand(f)
                    poly_f = f_exp.as_poly(x)
                    if poly_f is None:
                        num_factors = 0
                    else:
                        coeffs = poly_f.coeffs()
                        if all(c.is_rational for c in coeffs):
                            factors = sp.factor_list(f_exp, domain='QQ')[1]
                            num_factors = len(factors)
                        else:
                            num_factors = 0
                except Exception:
                    num_factors = 0
                    
                neg_q = bool(num_orbits != num_factors)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: L is a finite Galois extension of K with Galois group G",
    "H_3: R subset L is the set of roots of f",
    "not Q: The number of orbits of the action of G on R is not equal to the number of distinct irreducible factors of f in K"
]

N_HYP = 3
NEG_Q_INDEX = 3