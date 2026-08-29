import math

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def N(k, d):
    """
    Computes the number of 2x2 matrices over Z/kZ whose determinant is congruent to d (mod k).
    """
    count = 0
    for a in range(k):
        g = math.gcd(a, k)
        pairs_mod_g = 0
        for b in range(g):
            g_b = math.gcd(b, g)
            if d % g_b == 0:
                pairs_mod_g += g_b
        count += g * (k // g) * (k // g) * pairs_mod_g
    return count

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should provide (d, m, n).
    """
    try:
        if isinstance(witness, dict):
            d = witness.get('d')
            m = witness.get('m')
            n = witness.get('n')
        else:
            d, m, n = witness
    except Exception:
        return [False, False, False]
        
    # H_1: d is an integer
    try:
        h1 = isinstance(d, int) and not isinstance(d, bool)
    except Exception:
        h1 = False
        
    # H_2: m and n are positive integers (required for N(m) and N(n) to be well-defined)
    try:
        h2 = (isinstance(m, int) and not isinstance(m, bool) and m >= 1 and 
              isinstance(n, int) and not isinstance(n, bool) and n >= 1)
    except Exception:
        h2 = False
        
    # ¬Q: N(mn) != N(m)N(n)
    try:
        if h1 and h2:
            n_mn = N(m * n, d)
            n_m = N(m, d)
            n_n = N(n, d)
            neg_q = (n_mn != n_m * n_n)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: d is an integer",
    "H_2: m and n are positive integers",
    "¬Q: N(mn) != N(m)N(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2