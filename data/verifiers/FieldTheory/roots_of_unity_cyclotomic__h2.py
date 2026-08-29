import sympy
from sympy import Rational, Integer

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture.
    
    Conjecture:
      Hypothesis: n >= 1 is an integer
      Conclusion: The group of roots of unity contained in Q(zeta_n) has order 2n if n is odd, and order n if n is even.
      
    Wait, the conclusion is actually ALWAYS TRUE for all integers n >= 1.
    The roots of unity in Q(zeta_n) are exactly the 2n-th roots of unity if n is odd, and the n-th roots of unity if n is even.
    Since the prompt states this is a FALSE conjecture, and we must return a boolean for the negated conclusion,
    we will compute the actual number of roots of unity in Q(zeta_n) and check if it differs from the formula.
    (If the formula is always true, neg_Q will be False, but we implement the exact check as requested).
    """
    # Hypothesis 1: n >= 1 is an integer
    try:
        n = int(witness)
        h1 = (n >= 1 and n == witness)
    except Exception:
        h1 = False

    # Negated Conclusion: The group of roots of unity contained in Q(zeta_n) does NOT have order 2n (if n is odd) or n (if n is even).
    try:
        if not h1:
            neg_q = False
        else:
            # The number of roots of unity in Q(zeta_n) is the largest even integer W
            # such that the conductor of Q(zeta_W) divides the conductor of Q(zeta_n).
            def conductor(m):
                if m % 4 == 2:
                    return m // 2
                return m
            
            c_n = conductor(n)
            max_W = 1
            for W in range(2, 10 * n + 2, 2):
                if c_n % conductor(W) == 0:
                    max_W = max(max_W, W)
            
            expected_order = 2 * n if n % 2 == 1 else n
            
            # neg_q is True if the actual order differs from the expected order
            neg_q = (max_W != expected_order)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "not Q: The group of roots of unity contained in Q(zeta_n) does NOT have order 2n if n is odd, and order n if n is even"
]

N_HYP = 1
NEG_Q_INDEX = 1