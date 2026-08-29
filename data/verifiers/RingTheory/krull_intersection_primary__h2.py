import sympy
from sympy import ZZ, QQ, igcd
from sympy.abc import x, y, z
import functools

# Top-level setup
# ZZ and QQ are provided as standard commutative Noetherian domains.
# A typical witness would be (ZZ, [1]) or (QQ, [1]).

def is_comm_noeth_domain(R):
    if R in (ZZ, QQ, sympy.S.Integers, sympy.S.Rationals):
        return True
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        return is_comm_noeth_domain(R.domain)
    return False

def is_whole_ring(R, Q):
    try:
        iter(Q)
    except TypeError:
        Q = [Q]
    Q = list(Q)
    if not Q:
        return False
        
    if R in (ZZ, sympy.S.Integers):
        g = functools.reduce(igcd, Q)
        return abs(g) == 1
    if R in (QQ, sympy.S.Rationals):
        return any(q != 0 for q in Q)
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        try:
            gb = sympy.groebner(Q, *R.symbols, domain=R.domain)
            polys = list(gb)
            if len(polys) == 1:
                p = polys[0]
                if p == 1 or (hasattr(p, 'is_one') and p.is_one):
                    return True
        except Exception:
            pass
        return 1 in Q or any(getattr(q, 'is_one', False) or q == 1 for q in Q)
    return False

def conditions(witness):
    try:
        R, Q = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = bool(is_comm_noeth_domain(R))
    except Exception:
        h1 = False
        
    try:
        # In a commutative Noetherian domain, the intersection of Q^n is (0)
        # if and only if Q is a proper ideal (Krull's Intersection Theorem).
        # Thus, the intersection is NOT (0) if and only if Q is the whole ring.
        neg_q = bool(is_whole_ring(R, Q))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian domain",
    "¬Q: The intersection of all positive powers of Q is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1