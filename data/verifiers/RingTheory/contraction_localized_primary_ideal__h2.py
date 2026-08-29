import sympy
import math

# Top-level setup for Ring Theory
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a dictionary representing ideals in the ring of integers Z:
      - 'q': integer, generator of the ideal Q
      - 'p': integer, generator of the ideal P
      - 'S': list of integers, representing the subset S
    """
    try:
        q = witness['q']
        p = witness['p']
        S = witness['S']
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring with identity
    # We evaluate this in R = Z, which is always a commutative ring with identity.
    h1 = True

    # H_2: Q is a P-primary ideal of R
    # In Z, (q) is (p)-primary iff q = p^k for some k >= 1 and p is prime, or q = p = 0.
    try:
        if q == 0:
            h2 = (p == 0)
        else:
            if p == 0:
                h2 = False
            else:
                p_abs = abs(p)
                if not sympy.isprime(p_abs):
                    h2 = False
                else:
                    temp = abs(q)
                    if temp == 1:
                        h2 = False
                    else:
                        while temp % p_abs == 0:
                            temp //= p_abs
                        h2 = (temp == 1)
    except Exception:
        h2 = False

    # H_3: The prime ideal P is disjoint from S (P ∩ S = ∅)
    # In Z, this means no element of S is a multiple of p.
    try:
        h3 = True
        if p == 0:
            if 0 in S:
                h3 = False
        else:
            for s in S:
                if s % p == 0:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # ¬Q: The contraction of the extended ideal (S^{-1}Q)^c in R is NOT equal to Q.
    # The contraction C = {x \in Z | \exists s \in S, sx \in Q}.
    # If S is empty, C is empty. Since Q contains 0, Q is not empty, so C != Q.
    # If S is non-empty and disjoint from P, then C = Q.
    try:
        if len(S) == 0:
            neg_q = True
        else:
            neg_q = False
            for s in S:
                if q != 0 and math.gcd(s, q) > 1:
                    neg_q = True
                    break
                elif q == 0 and s == 0:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: Q is a P-primary ideal of R",
    "H_3: The prime ideal P is disjoint from S (P ∩ S = ∅)",
    "¬Q: The contraction of the extended ideal (S^{-1}Q)^c in R is not equal to Q"
]

N_HYP = 3
NEG_Q_INDEX = 3