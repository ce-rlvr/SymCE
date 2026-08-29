import sympy

# Top-level setup: named object bindings that the witness expression may reference.
x = sympy.Symbol('x')

class Ring:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

ZZ = Ring("ZZ")
QQ = Ring("QQ")
QQx = Ring("QQx")
ZZx = Ring("ZZx")

def is_comm_ring_with_id(R):
    return R in [ZZ, QQ, QQx, ZZx]

def is_subring(R, S):
    if R == S: 
        return True
    if R == ZZ and S in [QQ, ZZx, QQx]: 
        return True
    if R == QQ and S in [QQx]: 
        return True
    if R == ZZx and S in [QQx]: 
        return True
    return False

def is_prime_ideal(I, S):
    if S == ZZ:
        if I == 0: 
            return True
        try:
            return sympy.isprime(int(I))
        except Exception:
            return False
    if S == QQ:
        return I == 0
    if S == QQx:
        return I in [0, x]
    if S == ZZx:
        if I in [0, x]: 
            return True
        try:
            return sympy.isprime(int(I))
        except Exception:
            return False
    return False

def is_maximal_ideal(I, S):
    if S == ZZ:
        if I == 0: 
            return False
        try:
            return sympy.isprime(int(I))
        except Exception:
            return False
    if S == QQ:
        return I == 0
    if S == QQx:
        return I == x
    if S == ZZx:
        return False
    return False

def intersect(I, S, R):
    if not is_subring(R, S): 
        return None
    if R == S: 
        return I
    if S == QQ and R == ZZ:
        if I == 0: 
            return 0
    if S == QQx and R == QQ:
        if I == 0: 
            return 0
        if I == x: 
            return 0
    if S == QQx and R == ZZ:
        if I == 0: 
            return 0
        if I == x: 
            return 0
    if S == ZZx and R == ZZ:
        if I == 0: 
            return 0
        if I == x: 
            return 0
        try:
            if sympy.isprime(int(I)): 
                return I
        except Exception:
            pass
    return None

def conditions(witness) -> list[bool]:
    try:
        R, S, Q, P = witness
    except Exception:
        return [False] * 5
    
    try:
        h1 = is_comm_ring_with_id(R) and is_comm_ring_with_id(S)
    except Exception:
        h1 = False

    try:
        h2 = is_subring(R, S)
    except Exception:
        h2 = False

    try:
        h3 = is_prime_ideal(Q, S)
    except Exception:
        h3 = False

    try:
        h4 = (P == intersect(Q, S, R)) and (P is not None)
    except Exception:
        h4 = False

    try:
        q_max = is_maximal_ideal(Q, S)
        p_max = is_maximal_ideal(P, R)
        neg_Q = (q_max != p_max)
    except Exception:
        neg_Q = False

    return [h1, h2, h3, h4, neg_Q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: R is a subring of S",
    "H_3: Q is a prime ideal of S",
    "H_4: P = Q ∩ R",
    "¬Q: Q is maximal in S is not equivalent to P is maximal in R"
]

N_HYP = 4
NEG_Q_INDEX = 4