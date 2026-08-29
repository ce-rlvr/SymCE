import sympy
import math

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple or dictionary providing p, a, k, d.
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            a = witness.get('a')
            k = witness.get('k')
            d = witness.get('d')
        else:
            p, a, k, d = witness
    except Exception:
        return [False, False, False, False]

    # H1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H2: a is an integer such that gcd(a, p) = 1
    try:
        h2 = isinstance(a, int) and math.gcd(a, p) == 1
    except Exception:
        h2 = False

    # H3: d = gcd(k, p-1)
    try:
        h3 = d == math.gcd(k, p - 1)
    except Exception:
        h3 = False

    # Conclusion: The congruence x^k = a mod p has an integer solution iff a^((p-1)/d) = 1 mod p
    # We evaluate the negated conclusion (neg_Q).
    try:
        # Evaluate right side: a^((p-1)/d) = 1 mod p
        if (p - 1) % d != 0:
            right_side = False
        else:
            power = (p - 1) // d
            right_side = pow(a, power, p) == 1

        # Evaluate left side: x^k = a mod p has an integer solution
        # Note: If k is negative, x^k evaluated over integers is a fraction (unless x=1 or -1),
        # so it cannot be congruent to an integer a mod p in the strict sense of integer exponentiation.
        left_side = False
        for x in range(p):
            if k < 0:
                if x == 1:
                    val = 1
                elif x == p - 1 and k % 2 == 0:
                    val = 1
                elif x == p - 1 and k % 2 != 0:
                    val = -1
                else:
                    continue  # x^k is not an integer, so no integer solution in this strict sense
            else:
                val = pow(x, k)
            
            if val % p == a % p:
                left_side = True
                break
                
        # The conclusion is the iff statement. We want its negation.
        neg_q = (left_side != right_side)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: a is an integer such that gcd(a, p) = 1",
    "H_3: d = gcd(k, p-1)",
    "¬Q: The congruence x^k ≡ a (mod p) having an integer solution is NOT equivalent to a^((p-1)/d) ≡ 1 (mod p)"
]

N_HYP = 3
NEG_Q_INDEX = 3