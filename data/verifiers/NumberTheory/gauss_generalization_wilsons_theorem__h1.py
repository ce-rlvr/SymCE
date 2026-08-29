import math
from sympy import isprime

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    
    Remaining hypotheses:
      - Let n be of the form 4, p^k, or 2p^k, where p is an odd prime and k is a positive integer.
      - Let P be the product of all positive integers less than n that are coprime to n.
    
    Conclusion:
      - P ≡ -1 (mod n)
    """
    try:
        n = int(witness)
    except Exception:
        return [False, False, False]

    # Hypothesis 1: n is of the form 4, p^k, or 2p^k, where p is an odd prime and k is a positive integer.
    h1_ok = False
    try:
        if n == 4:
            h1_ok = True
        elif n > 2:
            # Check if n is of the form p^k or 2p^k
            target = n
            if target % 2 == 0:
                target //= 2
            
            # Find the prime factors of target
            factors = []
            temp = target
            d = 3
            while d * d <= temp:
                if temp % d == 0:
                    factors.append(d)
                    while temp % d == 0:
                        temp //= d
                d += 2
            if temp > 1:
                factors.append(temp)
            
            if len(factors) == 1:
                p = factors[0]
                if isprime(p) and p % 2 != 0:
                    # Check if target is exactly p^k
                    k = round(math.log(target, p))
                    if p**k == target and k >= 1:
                        h1_ok = True
    except Exception:
        h1_ok = False

    # Hypothesis 2: P is the product of all positive integers less than n that are coprime to n.
    # We compute P directly for the witness.
    h2_ok = False
    P = 1
    try:
        if h1_ok:
            for i in range(1, n):
                if math.gcd(i, n) == 1:
                    P *= i
            h2_ok = True
    except Exception:
        h2_ok = False

    # Conclusion: P ≡ -1 (mod n)
    # The negated conclusion is True if P is NOT congruent to -1 (mod n).
    neg_q_ok = False
    try:
        if h1_ok and h2_ok:
            if P % n != (n - 1) % n:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is of the form 4, p^k, or 2p^k, where p is an odd prime and k is a positive integer",
    "H_2: P is the product of all positive integers less than n that are coprime to n",
    "¬Q: P is not congruent to -1 (mod n)"
]

N_HYP = 2
NEG_Q_INDEX = 2