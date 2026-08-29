import sympy
import math

# Top-level setup
# The witness is expected to be a tuple (n, e) of two integers.
# This represents the ring R = Z_n and the ring homomorphism phi: Z -> Z_n given by phi(x) = e * x mod n.
# (If n = 0, R = Z).

def conditions(witness):
    try:
        n, e = witness
        n = int(n)
        e = int(e)
    except Exception:
        return [False, False]
        
    # H_1: R is a ring with multiplicative identity 1_R
    # Z_n is a ring with identity for any integer n.
    # We also verify that phi is a valid ring homomorphism from Z to Z_n.
    # This requires phi(x*y) = phi(x)*phi(y) => e*x*y = e^2*x*y mod n => e^2 = e mod n.
    try:
        if n == 0:
            h1 = (e * e == e)
        else:
            h1 = ((e * e) % n == e % n)
    except Exception:
        h1 = False
        
    # ¬Q: The kernel of phi is NOT the ideal nZ, where n is the characteristic of R.
    # For R = Z_n, the characteristic is abs(n).
    # The kernel of phi is kZ, where k is the smallest non-negative integer such that e*k = 0 mod n.
    # k = abs(n) / gcd(e, n). (If n=0, k=1 if e=0 else 0).
    try:
        if n == 0:
            k = 1 if e == 0 else 0
            char_R = 0
        else:
            k = abs(n) // math.gcd(e, n)
            char_R = abs(n)
            
        neg_q = (k != char_R)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with multiplicative identity 1_R",
    "¬Q: The kernel of phi is not the ideal nZ, where n is the characteristic of R"
]

N_HYP = 1
NEG_Q_INDEX = 1