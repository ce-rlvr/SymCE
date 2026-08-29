import sympy
import math

# Top-level setup for potential witness expressions
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Localization commutes with integral closure" (when S is not required to be multiplicative).
    
    Expected witness format:
    A tuple (R, K, L, A, S) or a dictionary with these keys.
    Example counterexample: ('ZZ', 'QQ', 'QQ', 'ZZ', [2])
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            K = witness.get('K')
            L = witness.get('L')
            A = witness.get('A')
            S = witness.get('S')
        else:
            R, K, L, A, S = witness
    except Exception:
        return [False] * 6

    def is_ZZ(x):
        if isinstance(x, str):
            return x.strip() in ['ZZ', 'Z']
        if x == sympy.S.Integers:
            return True
        return False

    def is_QQ(x):
        if isinstance(x, str):
            return x.strip() in ['QQ', 'Q']
        if x == sympy.S.Rationals:
            return True
        return False

    def lcm(a, b):
        return abs(a * b) // math.gcd(a, b) if a and b else 0

    # H_1: R is an integral domain
    try:
        h1 = is_ZZ(R) or is_QQ(R)
    except Exception:
        h1 = False

    # H_2: K is the field of fractions of R
    try:
        if is_ZZ(R):
            h2 = is_QQ(K)
        elif is_QQ(R):
            h2 = is_QQ(K)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: L is an algebraic field extension of K
    try:
        if is_QQ(K):
            h3 = is_QQ(L)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: A is the integral closure of R in L
    try:
        if is_ZZ(R) and is_QQ(L):
            h4 = is_ZZ(A)
        elif is_QQ(R) and is_QQ(L):
            h4 = is_QQ(A)
        else:
            h4 = False
    except Exception:
        h4 = False

    # H_5: 0 is not an element of S
    try:
        h5 = True
        # Ensure S is iterable
        iter(S)
        for s in S:
            if int(s) == 0:
                h5 = False
                break
    except Exception:
        h5 = False

    # ¬Q: S^{-1}A is not the integral closure of S^{-1}R in L
    # If S is not a multiplicative set, S^{-1}A is just a set of fractions {a/s | a in A, s in S}.
    # The integral closure of S^{-1}R in L is a ring.
    # For R=ZZ, A=ZZ, L=QQ, the set {a/s} equals the ring ZZ[1/s] if and only if 
    # the least common multiple of S is 1 (i.e., S only contains 1 or -1).
    # If lcm(S) > 1, S^{-1}A is not a ring, hence cannot be the integral closure.
    try:
        if is_ZZ(R) and is_ZZ(A) and is_QQ(L):
            m = 1
            for s in S:
                m = lcm(m, abs(int(s)))
            neg_q = (m > 1)
        elif is_QQ(R) and is_QQ(A) and is_QQ(L):
            neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: L is an algebraic field extension of K",
    "H_4: A is the integral closure of R in L",
    "H_5: 0 is not an element of S",
    "¬Q: S^{-1}A is not the integral closure of S^{-1}R in L"
]

N_HYP = 5
NEG_Q_INDEX = 5