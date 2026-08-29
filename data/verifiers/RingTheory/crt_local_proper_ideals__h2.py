import sympy
import math

# Top-level setup
# Witnesses are expected to be tuples (n, gen_I, gen_J) representing
# the ring R = Z/nZ, and ideals I = <gen_I>, J = <gen_J>.

def conditions(witness) -> list[bool]:
    try:
        n, gen_I, gen_J = witness
    except Exception:
        return [False, False, False]
        
    def get_gcd(gen, n_val):
        if isinstance(gen, (list, tuple, set)):
            g = int(n_val)
            for x in gen:
                g = math.gcd(g, int(x))
            return g
        else:
            return math.gcd(int(gen), int(n_val))

    # H_1: R is a local ring with a unique maximal ideal
    # In Z/nZ, the ring is local iff n is a prime power (n > 1).
    try:
        n_int = int(n)
        if n_int <= 1:
            h1 = False
        else:
            factors = sympy.factorint(n_int)
            h1 = (len(factors) == 1)
    except Exception:
        h1 = False

    # H_2: J is a proper ideal of R
    # In Z/nZ, J is proper iff gcd(gen_J, n) > 1.
    try:
        gcd_J = get_gcd(gen_J, n_int)
        h2 = (gcd_J > 1)
    except Exception:
        h2 = False

    # ¬Q: I and J are comaximal
    # In Z/nZ, I and J are comaximal iff I + J = R, which means gcd(gen_I, gen_J, n) == 1.
    try:
        gcd_I = get_gcd(gen_I, n_int)
        gcd_J = get_gcd(gen_J, n_int)
        neg_q = (math.gcd(gcd_I, gcd_J) == 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a local ring with a unique maximal ideal",
    "H_2: J is a proper ideal of R",
    "¬Q: The ideals I and J are comaximal"
]

N_HYP = 2
NEG_Q_INDEX = 2