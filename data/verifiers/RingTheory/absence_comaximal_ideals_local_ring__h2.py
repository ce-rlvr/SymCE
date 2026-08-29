import sympy
from sympy.ntheory import factorint
from math import gcd

# Top-level setup
# We use integers to represent the ring Z/nZ and its ideals.
# A witness should be a tuple (n, I, J) where n is the modulus (a prime power for a local ring),
# and I, J are integers or lists of integers representing the generators of the ideals.

def conditions(witness) -> list[bool]:
    try:
        n, I, J = witness
        n = int(n)
    except Exception:
        return [False, False]
        
    # H_1: R is a local ring with a unique maximal ideal M
    try:
        # Z/nZ is a local ring iff n is a prime power p^k (k >= 1)
        h1 = (n > 1 and len(factorint(n)) == 1)
    except Exception:
        h1 = False
        
    # ¬Q: I and J are comaximal (I + J = R)
    try:
        def get_gen(ideal):
            try:
                val = int(ideal)
                return gcd(val, n)
            except Exception:
                g = n
                for x in ideal:
                    g = gcd(g, int(x))
                return g
        
        i_gen = get_gen(I)
        j_gen = get_gen(J)
        
        # I + J = R in Z/nZ iff gcd(i_gen, j_gen, n) == 1
        neg_q = (gcd(gcd(i_gen, j_gen), n) == 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a local ring",
    "¬Q: I and J are comaximal (I + J = R)"
]

N_HYP = 1
NEG_Q_INDEX = 1