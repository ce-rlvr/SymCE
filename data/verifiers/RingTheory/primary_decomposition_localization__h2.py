import math
from sympy.ntheory import isprime

# Top-level setup
# For this domain (commutative rings and localizations), we evaluate the witness 
# in the ring of integers Z. Ideals are represented by their integer generators.
# The witness is expected to be a dictionary with keys:
# 'I': int (generator of ideal I)
# 'Q': list[int] (generators of primary components Q_i)
# 'P': list[int] (generators of prime radicals P_i)
# 'S': list[int] (elements of the subset S)
# 'm': int (number of components disjoint from S)

def get_lcm(lst):
    if not lst:
        return 1
    res = abs(lst[0])
    for x in lst[1:]:
        if res == 0 or x == 0:
            return 0
        res = (res * abs(x)) // math.gcd(res, abs(x))
    return res

def conditions(witness):
    try:
        I = witness['I']
        Q = witness['Q']
        P = witness['P']
        S = witness['S']
        m = witness['m']
    except Exception:
        return [False, False, False, False]
        
    # H_1: R is a commutative ring with identity
    # We use R = Z, which is always a commutative ring with identity.
    h1 = True
    
    # H_2: I is a proper ideal of R with a minimal primary decomposition I = \cap_{i=1}^n Q_i
    h2 = False
    try:
        if isinstance(I, int) and abs(I) != 1:
            n = len(Q)
            if n > 0 and len(P) == n:
                # Check I = \cap Q_i (in Z, intersection of ideals is the lcm of their generators)
                if abs(I) == get_lcm(Q):
                    # Check each Q_i is primary and P_i is its radical
                    primary_ok = True
                    for i in range(n):
                        q = abs(Q[i])
                        p = abs(P[i])
                        if q == 1 or p == 1:
                            primary_ok = False
                            break
                        if q == 0:
                            if p != 0:
                                primary_ok = False
                                break
                        else:
                            if not isprime(p):
                                primary_ok = False
                                break
                            # q must be a power of p
                            temp = q
                            while temp % p == 0:
                                temp //= p
                            if temp != 1:
                                primary_ok = False
                                break
                    if primary_ok:
                        # Check minimal: distinct radicals
                        if len(set(abs(p) for p in P)) == n:
                            # Check minimal: no Q_i can be omitted
                            minimal_ok = True
                            for i in range(n):
                                omit_lcm = get_lcm(Q[:i] + Q[i+1:])
                                if omit_lcm == abs(I):
                                    minimal_ok = False
                                    break
                            if minimal_ok:
                                h2 = True
    except Exception:
        h2 = False

    # H_3: The primary components are ordered such that P_i \cap S = \emptyset for 1 \le i \le m 
    # and P_i \cap S \neq \emptyset for m < i \le n
    h3 = False
    try:
        if 0 <= m <= len(Q):
            order_ok = True
            for i in range(len(Q)):
                p = abs(P[i])
                # P_i \cap S \neq \emptyset iff there is some s in S such that p divides s
                if p == 0:
                    intersects = (0 in S)
                else:
                    intersects = any(s % p == 0 for s in S)
                    
                if i < m:
                    if intersects:
                        order_ok = False
                        break
                else:
                    if not intersects:
                        order_ok = False
                        break
            if order_ok:
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: The extended ideal S^{-1}I does not have a minimal primary decomposition S^{-1}I = \cap_{i=1}^m S^{-1}Q_i
    # The conclusion fails if S is not a multiplicatively closed subset (so S^{-1}R is not a ring)
    # or if m = 0 (so S^{-1}I = S^{-1}R, which is not a proper ideal and thus has no primary decomposition).
    neg_q = False
    try:
        is_mult_closed = True
        if 1 not in S:
            is_mult_closed = False
        else:
            for a in S:
                for b in S:
                    if a * b not in S:
                        is_mult_closed = False
                        break
                if not is_mult_closed:
                    break
                    
        if not is_mult_closed or m == 0:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a proper ideal of R with a minimal primary decomposition I = \\cap_{i=1}^n Q_i",
    "H_3: The primary components are ordered such that P_i \\cap S = \\emptyset for 1 \\le i \\le m and P_i \\cap S \\neq \\emptyset for m < i \\le n",
    "¬Q: The extended ideal S^{-1}I does not have a minimal primary decomposition S^{-1}I = \\cap_{i=1}^m S^{-1}Q_i in the localized ring S^{-1}R"
]

N_HYP = 3
NEG_Q_INDEX = 3