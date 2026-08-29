import sympy
import functools

# Top-level setup
Z = sympy.ZZ
Q = sympy.QQ

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I, J, and K are ideals of R",
    "H_3: I is an invertible ideal",
    "¬Q: J != K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        R, I, J, K = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: R is a commutative ring
    try:
        h1 = getattr(R, 'is_commutative', False)
        if not h1 and R in (sympy.ZZ, sympy.QQ):
            h1 = True
    except Exception:
        h1 = False
        
    # H2: I, J, K are ideals of R
    try:
        def is_ideal(ring, ideal):
            if not isinstance(ideal, (list, tuple, set)):
                return False
            return all(e in ring for e in ideal)
        h2 = is_ideal(R, I) and is_ideal(R, J) and is_ideal(R, K)
    except Exception:
        h2 = False
        
    # H3: I is an invertible ideal
    try:
        def is_invertible(ring, ideal):
            if not ideal: 
                return False
            if all(e == 0 for e in ideal): 
                return False
            if ring in (sympy.ZZ, sympy.QQ):
                return True
            if len(ideal) == 1 and getattr(ring, 'is_domain', False):
                return True
            if hasattr(ring, 'gens') and len(ring.gens) == 1 and getattr(ring.domain, 'is_Field', False):
                return True
            return False
        h3 = is_invertible(R, I)
    except Exception:
        h3 = False
        
    # ¬Q: J != K
    try:
        def ideals_equal(ring, id1, id2):
            if ring == sympy.ZZ:
                gcd1 = functools.reduce(sympy.gcd, id1, 0)
                gcd2 = functools.reduce(sympy.gcd, id2, 0)
                return abs(gcd1) == abs(gcd2)
            if ring == sympy.QQ:
                z1 = all(e == 0 for e in id1)
                z2 = all(e == 0 for e in id2)
                return z1 == z2
            if hasattr(ring, 'gens'):
                from sympy import groebner
                try:
                    gb1 = groebner(id1, ring.gens, domain=ring.domain)
                    gb2 = groebner(id2, ring.gens, domain=ring.domain)
                    return gb1 == gb2
                except Exception:
                    pass
            return set(id1) == set(id2)
        neg_q = not ideals_equal(R, J, K)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]