import sympy
from sympy.ntheory import totient, primefactors

# Top-level setup
# (No specific named bindings required for Number Theory / Field Theory witnesses; integers are used directly)

def v(q, m):
    """Return the exact highest power of prime q dividing m."""
    if m == 0:
        return 0
    m = abs(m)
    ans = 0
    while m % q == 0:
        ans += 1
        m //= q
    return ans

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture.
    Witness is expected to be a tuple: (n, p, k)
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        n, p, k = witness
    except Exception:
        return [False, False, False]
        
    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n >= 1
    except Exception:
        h1 = False
        
    # H_2: p^k is the exact highest power of p that divides n
    try:
        h2 = False
        if isinstance(p, (int, sympy.Integer)) and isinstance(k, (int, sympy.Integer)):
            if p >= 2 and k >= 0:
                if (n % (p**k) == 0) and (n % (p**(k+1)) != 0):
                    h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: The ramification index of some prime ideal lying over p in Q(zeta_n) is NOT exactly phi(p^k)
    # The ramification index of a prime ideal lying over p (which lies over some prime factor q of p)
    # in the cyclotomic field Q(zeta_n) over Q is given by phi(q^{v_q(n)}).
    try:
        neg_q = False
        if h1 and h2:
            expected = totient(p**k)
            for q in primefactors(p):
                vq_n = v(q, n)
                e_Q = totient(q**vq_n)
                if e_Q != expected:
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: p^k is the exact highest power of p that divides n",
    "¬Q: The ramification index of some prime ideal lying over p in Q(zeta_n) is not exactly phi(p^k)"
]

N_HYP = 2
NEG_Q_INDEX = 2