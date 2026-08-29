import math
import sympy

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - gcd(x, y) == 1
      - p is an odd prime
      - p divides x^2 + y^2
    Conclusion:
      - p ≡ 1 (mod 4)
    """
    try:
        if isinstance(witness, dict):
            x = witness.get('x')
            y = witness.get('y')
            p = witness.get('p')
        else:
            x, y, p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: gcd(x, y) == 1
    try:
        h1 = (math.gcd(int(x), int(y)) == 1)
    except Exception:
        h1 = False

    # H_2: p is an odd prime
    try:
        p_int = int(p)
        h2 = sympy.isprime(p_int) and (p_int % 2 != 0)
    except Exception:
        h2 = False

    # H_3: p divides x^2 + y^2
    try:
        h3 = ((int(x)**2 + int(y)**2) % int(p) == 0)
    except Exception:
        h3 = False

    # ¬Q: p is not congruent to 1 mod 4
    try:
        neg_q = (int(p) % 4 != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: gcd(x, y) == 1",
    "H_2: p is an odd prime",
    "H_3: p divides x^2 + y^2",
    "¬Q: p is not congruent to 1 mod 4"
]

N_HYP = 3
NEG_Q_INDEX = 3