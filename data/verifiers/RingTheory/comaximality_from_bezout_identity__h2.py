import sympy
from sympy import S
from sympy.polys.domains import ZZ, QQ, RR, CC

# Top-level setup
Z_set = S.Integers
Q_set = S.Rationals
R_set = S.Reals
C_set = S.Complexes

def in_R(val, R):
    try:
        if hasattr(R, 'contains'):
            res = R.contains(val)
            if res is True or res is False:
                return bool(res)
        if hasattr(R, '__contains__'):
            try:
                if val in R:
                    return True
            except Exception:
                pass
    except Exception:
        pass
    return False

def is_comm_ring_with_id(R):
    try:
        if R in (S.Integers, S.Rationals, S.Reals, S.Complexes):
            return True
        from sympy.polys.domains.domain import Domain
        if isinstance(R, Domain):
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The dropped hypothesis is that a, b \in R.
    If a or b is not in R, they do not generate valid principal ideals in R, 
    making the conclusion false.
    """
    try:
        if len(witness) == 5:
            R, a, b, x, y = witness
        elif len(witness) == 4:
            a, b, x, y = witness
            R = S.Integers
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
    
    # H1: R is a commutative ring with identity
    try:
        h1 = is_comm_ring_with_id(R)
    except Exception:
        h1 = False
        
    # H2: x, y \in R
    try:
        h2 = in_R(x, R) and in_R(y, R)
    except Exception:
        h2 = False
        
    # H3: ax + by = 1
    try:
        h3 = bool(sympy.simplify(a*x + b*y - 1) == 0)
    except Exception:
        h3 = False
        
    # neg_Q: The principal ideals (a) and (b) are NOT comaximal in R
    # This holds if a or b is not in R (so they don't form principal ideals in R).
    # If a, b \in R, then ax+by=1 mathematically guarantees they are comaximal.
    try:
        neg_q = not (in_R(a, R) and in_R(b, R))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: x and y are elements of R",
    "H_3: ax + by = 1",
    "¬Q: The principal ideals (a) and (b) are not comaximal in R (e.g., a or b is not in R)"
]

N_HYP = 3
NEG_Q_INDEX = 3