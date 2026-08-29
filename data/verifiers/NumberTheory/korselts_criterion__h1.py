import sympy
from sympy.ntheory import factorint, primefactors

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture:
    'a^n ≡ a (mod n) for all integers a if and only if n is square-free 
    and p-1 divides n-1 for every prime factor p of n.'
    """
    try:
        n = int(witness)
    except Exception:
        return [False]
    
    # Evaluate P(n): a^n ≡ a (mod n) for all integers a
    try:
        if n <= 0:
            # For n <= 0, a^n is not an integer for a >= 2, so the congruence 
            # a^n ≡ a (mod n) is either undefined or false for all integers a.
            P_n = False
        else:
            P_n = True
            # Test a range of values to verify P(n). 
            # Testing up to 200 and all prime factors is more than enough to find a counterexample if P(n) is false.
            test_a = set(range(min(n + 1, 200)))
            try:
                for p in primefactors(n):
                    test_a.add(p)
            except Exception:
                pass
            
            for a in test_a:
                if pow(a, n, n) != a % n:
                    P_n = False
                    break
    except Exception:
        P_n = False

    # Evaluate Q(n): n is square-free and p-1 | n-1 for all prime factors p of n
    try:
        if n == 0:
            Q_n = False
        else:
            # Check if n is square-free
            factors = factorint(abs(n))
            is_sq_free = all(v == 1 for k, v in factors.items() if k != -1)
            
            if not is_sq_free:
                Q_n = False
            else:
                Q_n = True
                for p in primefactors(abs(n)):
                    if (n - 1) % (p - 1) != 0:
                        Q_n = False
                        break
    except Exception:
        Q_n = False

    # The conjecture states P(n) <=> Q(n).
    # The negated conclusion is that P(n) is NOT equivalent to Q(n).
    neg_q = bool(P_n != Q_n)
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: a^n ≡ a (mod n) for all a is NOT equivalent to n being square-free and p-1 | n-1 for all p|n"
]
N_HYP = 0
NEG_Q_INDEX = 0