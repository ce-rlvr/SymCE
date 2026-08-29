import sympy
from sympy import gcd, factorint

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture.
    The witness should be a tuple: (q, a, n)
    where:
      - q is the order of the finite field F (must be a prime power)
      - a is a non-zero element of F (represented as an integer)
      - n is the degree of the Dickson polynomial
    """
    try:
        q, a, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a finite field of order q
    try:
        if not isinstance(q, int) or q < 2:
            h1 = False
        else:
            factors = factorint(q)
            h1 = len(factors) == 1
    except Exception:
        h1 = False

    # H_2: a is a non-zero element of F
    try:
        if h1:
            p = list(factorint(q).keys())[0]
            if q == p:
                a_val = int(a) % q
                h2 = a_val != 0
            else:
                if isinstance(a, int):
                    h2 = (a % p) != 0
                else:
                    h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: D_n(x, a) is the n-th Dickson polynomial of the first kind over F
    try:
        h3 = isinstance(n, int) and n >= 0
    except Exception:
        h3 = False

    # neg_Q: The conclusion FAILS at the witness.
    try:
        neg_q_ok = False
        if h1 and h2 and h3:
            p = list(factorint(q).keys())[0]
            
            if q == p:
                a_val = int(a) % q
                
                def eval_dickson(val, n, a_val, p):
                    if n == 0:
                        return 2 % p
                    if n == 1:
                        return val % p
                    d_prev2 = 2 % p
                    d_prev1 = val % p
                    for _ in range(2, n + 1):
                        d_curr = (val * d_prev1 - a_val * d_prev2) % p
                        d_prev2 = d_prev1
                        d_prev1 = d_curr
                    return d_prev1

                images = set()
                for val in range(q):
                    images.add(eval_dickson(val, n, a_val, q))
                
                is_permutation = len(images) == q
                gcd_cond = gcd(n, q**2 - 1) == 1
                
                neg_q_ok = is_permutation != gcd_cond
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1, h2, h3, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "H_2: a is a non-zero element of F",
    "H_3: D_n(x, a) is the n-th Dickson polynomial of the first kind over F",
    "¬Q: D_n(x, a) induces a permutation on F is NOT equivalent to gcd(n, q^2 - 1) = 1"
]

N_HYP = 3
NEG_Q_INDEX = 3