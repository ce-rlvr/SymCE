import math
from sympy.ntheory import factorint, isprime

def is_primary(q):
    if q == 0: return True
    if abs(q) == 1: return False
    factors = factorint(abs(q))
    return len(factors) == 1

def radical(q):
    if q == 0: return 0
    factors = factorint(abs(q))
    rad = 1
    for p in factors:
        rad *= p
    return rad

def intersect_S_empty(P, S_type, S_val):
    if P == 0:
        if S_type == 'complement':
            return True
        elif S_type == 'generated':
            return S_val != 0
        else:
            raise ValueError("Unknown S_type")
    if S_type == 'complement':
        if S_val == 0:
            return False
        return P % S_val == 0
    elif S_type == 'generated':
        if S_val == 0:
            return False
        if abs(S_val) == 1:
            return abs(P) != 1
        factors_P = factorint(abs(P))
        for p in factors_P:
            if S_val % p != 0:
                return True
        return False
    else:
        raise ValueError("Unknown S_type")

def saturate(A, S_type, S_val):
    if S_type == 'generated' and S_val == 0:
        return 1
    if S_type == 'complement' and S_val == 0:
        if A == 0: return 0
        return 1
    if A == 0: return 0
    A = abs(A)
    if S_type == 'complement':
        k = 0
        while A % S_val == 0:
            k += 1
            A //= S_val
        return abs(S_val)**k
    elif S_type == 'generated':
        factors = factorint(A)
        res = 1
        for p, k in factors.items():
            if S_val % p != 0:
                res *= p**k
        return res
    else:
        raise ValueError("Unknown S_type")

def is_multiple(B, A):
    if A == 0:
        return B == 0
    return B % A == 0

def conditions(witness):
    try:
        h1 = (witness.get('ring') == 'Z')
    except Exception:
        h1 = False

    try:
        S_type = witness.get('S_type')
        S_val = witness.get('S_val')
        if S_type == 'complement':
            h2 = isprime(abs(S_val)) or S_val == 0
        elif S_type == 'generated':
            h2 = isinstance(S_val, int)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        Q = witness.get('Q', [])
        P = witness.get('P', [])
        m = witness.get('m', 0)
        n = len(Q)
        
        h3 = True
        if not (0 <= m <= n):
            h3 = False
        elif len(P) != n:
            h3 = False
        else:
            for i in range(n):
                if not is_primary(Q[i]):
                    h3 = False
                    break
                if abs(P[i]) != radical(Q[i]):
                    h3 = False
                    break
                empty_intersection = intersect_S_empty(P[i], S_type, S_val)
                if i < m:
                    if not empty_intersection:
                        h3 = False
                        break
                else:
                    if empty_intersection:
                        h3 = False
                        break
    except Exception:
        h3 = False

    try:
        I = witness.get('I', 0)
        Q = witness.get('Q', [])
        P = witness.get('P', [])
        m = witness.get('m', 0)
        S_type = witness.get('S_type')
        S_val = witness.get('S_val')
        
        if not (0 <= m <= len(Q)):
            raise ValueError("Invalid m")
            
        lhs_gen = saturate(I, S_type, S_val)
        
        if m == 0:
            rhs_gen = 1
        else:
            rhs_gen = abs(Q[0])
            for i in range(1, m):
                if rhs_gen == 0 or Q[i] == 0:
                    rhs_gen = 0
                else:
                    rhs_gen = (rhs_gen * abs(Q[i])) // math.gcd(rhs_gen, abs(Q[i]))
            rhs_gen = saturate(rhs_gen, S_type, S_val)
            
        eq = (abs(lhs_gen) == abs(rhs_gen))
        
        minimal = True
        if m > 0:
            rads = [abs(P[i]) for i in range(m)]
            if len(set(rads)) != len(rads):
                minimal = False
            for j in range(m):
                if m == 1:
                    break
                lcm_others = 1
                first = True
                for i in range(m):
                    if i != j:
                        if first:
                            lcm_others = abs(Q[i])
                            first = False
                        else:
                            if lcm_others == 0 or Q[i] == 0:
                                lcm_others = 0
                            else:
                                lcm_others = (lcm_others * abs(Q[i])) // math.gcd(lcm_others, abs(Q[i]))
                if is_multiple(lcm_others, abs(Q[j])):
                    minimal = False
                    break
                    
        concl = eq and minimal
        neg_q = not concl
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: The primary components are ordered such that P_i ∩ S = ∅ for 1 ≤ i ≤ m and P_i ∩ S ≠ ∅ for m < i ≤ n, where P_i = √Q_i",
    "¬Q: The extended ideal S^{-1}I does not have the minimal primary decomposition S^{-1}I = ∩_{i=1}^m S^{-1}Q_i"
]

N_HYP = 3
NEG_Q_INDEX = 3