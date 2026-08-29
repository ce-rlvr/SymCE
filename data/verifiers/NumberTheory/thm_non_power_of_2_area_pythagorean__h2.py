import math

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    
    Remaining hypotheses:
      - (a, b, c) is a Pythagorean triple consisting of positive integers
    
    Conclusion (must FAIL at the witness):
      - There does not exist a non-negative integer k such that A = 2^k.
      (where A is the area of the Pythagorean triangle)
    """
    try:
        a, b, c = witness
    except Exception:
        return [False, False]
    
    # H_1: (a, b, c) is a Pythagorean triple consisting of positive integers
    try:
        h1_ok = (
            isinstance(a, int) and isinstance(b, int) and isinstance(c, int) and
            a > 0 and b > 0 and c > 0 and
            a**2 + b**2 == c**2
        )
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion FAILS at the witness.
    # This means there EXISTS a non-negative integer k such that A = 2^k.
    # The area of a Pythagorean triangle is A = (a * b) / 2.
    try:
        if (a * b) % 2 != 0:
            neg_q_ok = False
        else:
            A = (a * b) // 2
            # Check if A is a power of 2 (i.e., A = 2^k for some non-negative integer k)
            if A <= 0:
                neg_q_ok = False
            else:
                # A is a power of 2 iff (A & (A - 1)) == 0
                neg_q_ok = (A & (A - 1)) == 0
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (a, b, c) is a Pythagorean triple consisting of positive integers",
    "¬Q: There exists a non-negative integer k such that A = 2^k"
]

N_HYP = 1
NEG_Q_INDEX = 1