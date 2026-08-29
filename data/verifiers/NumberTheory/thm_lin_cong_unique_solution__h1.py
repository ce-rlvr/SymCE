import math

CONDITION_LABELS = [
    "H_1: gcd(a, m) == 1",
    "¬Q: The linear congruence ax ≡ b (mod m) does NOT have exactly one solution modulo m"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (a, b, m), checks if it is a counterexample to the conjecture:
    "If gcd(a, m) = 1, then ax ≡ b (mod m) has exactly one solution modulo m."
    
    The dropped hypothesis is likely m > 0 or m != 0.
    If m = 0, the congruence is ax = b.
    If m = 0 and a = 1, b = 0, then 1*x = 0 has exactly one solution (x = 0).
    Wait, if m = 0, modulo 0 means equality. So x = b is exactly one solution.
    Wait, what if m = 0 and a = 1, b = 1? x = 1. Exactly one solution.
    What if m = 0 and a = 0? gcd(0, 0) = 0 != 1.
    What if m = 0 and a = -1? -x = b => x = -b. Exactly one solution.
    Wait, what if m = 1? gcd(a, 1) = 1. ax ≡ b (mod 1). All x are solutions.
    Modulo 1, all integers are congruent, so there is exactly 1 solution modulo 1.
    
    Let's carefully count solutions modulo m.
    If m != 0, we check x in 0, 1, ..., |m|-1.
    If m == 0, we check x in Z. Since ax = b, if a != 0, there is at most 1 solution.
    If a = 0, gcd(0, 0) = 0 != 1.
    So for m = 0, there is always exactly 1 solution in Z if a = 1 or -1, which are the only cases where gcd(a, 0) = 1.
    Wait, if a = 1, b = 0, m = 0, there is 1 solution.
    Is it possible the witness is a tuple of polynomials? No, NumberTheory domain.
    What if the witness is a tuple (a, b, m) where m < 0?
    If m < 0, modulo m is the same as modulo |m|.
    What if the witness is a tuple (a, b, m) where m is not an integer?
    Let's assume the witness is a tuple of integers (a, b, m).
    """
    try:
        a, b, m = witness
        if not (isinstance(a, int) and isinstance(b, int) and isinstance(m, int)):
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: gcd(a, m) == 1
    try:
        h1 = math.gcd(a, m) == 1
    except Exception:
        h1 = False

    # ¬Q: The linear congruence ax ≡ b (mod m) does NOT have exactly one solution modulo m
    try:
        if m == 0:
            # Modulo 0 means equality: ax = b
            # Solutions are integers x such that ax = b
            if a == 0:
                if b == 0:
                    # infinitely many solutions
                    num_solutions = float('inf')
                else:
                    num_solutions = 0
            else:
                if b % a == 0:
                    num_solutions = 1
                else:
                    num_solutions = 0
        else:
            # Modulo m != 0
            # We count solutions in the range 0 <= x < |m|
            abs_m = abs(m)
            num_solutions = 0
            for x in range(abs_m):
                if (a * x - b) % abs_m == 0:
                    num_solutions += 1
                    
        neg_q = num_solutions != 1
    except Exception:
        neg_q = False

    return [h1, neg_q]