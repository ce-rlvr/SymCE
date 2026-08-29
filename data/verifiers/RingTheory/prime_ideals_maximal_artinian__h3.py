import math
from sympy import S, gcd, factor_list, isprime
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y

# Top-level setup for potential witness expressions
Z = ZZ
Q = QQ
Qx = QQ[x]
Zx = ZZ[x]

def is_commutative_ring(R):
    return R in (ZZ, QQ, Qx, Zx, S.Integers, S.Rationals)

def has_identity(R):
    return R in (ZZ, QQ, Qx, Zx, S.Integers, S.Rationals)

def normalize_ideal(P):
    if isinstance(P, (list, tuple, set)):
        return list(P)
    return [P]

def to_expr(p):
    try:
        return p.as_expr()
    except Exception:
        return p

def is_int(e):
    return isinstance(e, int) or (hasattr(e, 'is_Integer') and e.is_Integer)

def is_prime_ideal(R, P):
    P = normalize_ideal(P)
    if R in (ZZ, S.Integers):
        g = 0
        for p in P:
            try:
                g = math.gcd(g, int(p))
            except Exception:
                return False
        g = abs(g)
        if g == 0:
            return True
        return isprime(g)
    elif R in (QQ, S.Rationals):
        return all(p == 0 for p in P)
    elif R in (Qx, Zx):
        exprs = [to_expr(p) for p in P]
        if all(e == 0 for e in exprs):
            return True
        
        if R == Qx:
            g = 0
            for e in exprs:
                if e != 0:
                    if g == 0:
                        g = e
                    else:
                        g = gcd(g, e)
            if g == 0:
                return True
            try:
                factors = factor_list(g)
                return len(factors[1]) == 1 and factors[1][0][1] == 1
            except Exception:
                return False
                
        if R == Zx:
            if len(exprs) == 1:
                e = exprs[0]
                if is_int(e):
                    return isprime(int(e))
                try:
                    factors = factor_list(e)
                    if len(factors[1]) == 1 and factors[1][0][1] == 1 and abs(factors[0]) == 1:
                        return True
                except Exception:
                    pass
            if len(exprs) == 2:
                e1, e2 = exprs
                if (is_int(e1) and e2 == x) or (is_int(e2) and e1 == x):
                    prime_cand = e1 if is_int(e1) else e2
                    return isprime(int(prime_cand))
            return False
    return False

def is_maximal_ideal(R, P):
    P = normalize_ideal(P)
    if R in (ZZ, S.Integers):
        g = 0
        for p in P:
            try:
                g = math.gcd(g, int(p))
            except Exception:
                return False
        g = abs(g)
        return isprime(g)
    elif R in (QQ, S.Rationals):
        return all(p == 0 for p in P)
    elif R == Qx:
        exprs = [to_expr(p) for p in P]
        if all(e == 0 for e in exprs):
            return False
        g = 0
        for e in exprs:
            if e != 0:
                if g == 0:
                    g = e
                else:
                    g = gcd(g, e)
        try:
            factors = factor_list(g)
            return len(factors[1]) == 1 and factors[1][0][1] == 1
        except Exception:
            return False
    elif R == Zx:
        exprs = [to_expr(p) for p in P]
        if all(e == 0 for e in exprs):
            return False
        if len(exprs) == 1:
            return False
        if len(exprs) == 2:
            e1, e2 = exprs
            if (is_int(e1) and e2 == x) or (is_int(e2) and e1 == x):
                prime_cand = e1 if is_int(e1) else e2
                return isprime(int(prime_cand))
        return False
    return False

def conditions(witness):
    try:
        R, P = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = is_commutative_ring(R)
    except Exception:
        h1 = False
        
    try:
        h2 = has_identity(R)
    except Exception:
        h2 = False
        
    try:
        h3 = is_prime_ideal(R, P)
    except Exception:
        h3 = False
        
    try:
        neg_q = not is_maximal_ideal(R, P)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "H_3: P is a prime ideal of R",
    "¬Q: P is not a maximal ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3