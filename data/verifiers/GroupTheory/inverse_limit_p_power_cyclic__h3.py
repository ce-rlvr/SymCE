import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to define the prime `p` and the transition maps `c`.
    Since G_n = Z/p^nZ, a homomorphism G_{n+1} -> G_n is uniquely determined by 
    the image of 1, which we denote as c_n. Thus, the inverse system is fully 
    parameterized by a sequence of integers c_n.
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            p, c = witness
        elif hasattr(witness, 'p') and hasattr(witness, 'c'):
            p = witness.p
            c = witness.c
        elif hasattr(witness, 'p') and hasattr(witness, 'transition_maps'):
            p = witness.p
            c = witness.transition_maps
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def get_c(n):
        if callable(c):
            return c(n)
        elif isinstance(c, dict):
            return c[n]
        else:
            return c[n - 1]

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: {G_n} is an inverse system of groups where G_n = Z/p^nZ
    # This holds if the transition maps are well-defined homomorphisms,
    # which is true for any integer multiplier c_n.
    try:
        h2 = True
        count = 0
        for n in range(1, 20):
            try:
                val = get_c(n)
                count += 1
            except (IndexError, KeyError):
                break
            if not isinstance(val, (int, sympy.Integer)):
                h2 = False
                break
        if count == 0:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The inverse limit of {G_n} is NOT isomorphic to Z_p
    # The inverse limit is isomorphic to Z_p iff the p-adic valuation of the 
    # transition multipliers c_n is 0 for all but finitely many n.
    # If the valuation grows indefinitely, the inverse limit is {0}, which is not Z_p.
    # We check if the inverse limit is {0} by verifying that for each k, 
    # there exists N > k such that the map G_N -> G_k is zero (i.e., p^k divides the product).
    try:
        neg_q = True
        for k in range(1, 11):
            prod = 1
            found_N = False
            for N in range(k + 1, k + 100):
                try:
                    val = get_c(N - 1)
                except (IndexError, KeyError):
                    break
                prod *= val
                if p == 0:
                    break
                if prod % (p**k) == 0:
                    found_N = True
                    break
            if not found_N:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: {G_n} is an inverse system of groups where G_n = Z/p^nZ",
    "¬Q: The inverse limit of {G_n} is not isomorphic to Z_p"
]

N_HYP = 2
NEG_Q_INDEX = 2