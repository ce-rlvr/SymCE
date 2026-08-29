import sympy
import math

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    
    Conjecture:
      Hypotheses:
        - a and b are integers, not both zero
      Conclusion:
        - d divides both a and b if and only if d divides gcd(a, b)
        
    The witness should be a tuple (a, b, d).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False]
        a, b, d = witness
    except Exception:
        return [False, False]

    # H1: a and b are integers, not both zero
    try:
        a_is_int = isinstance(a, (int, sympy.Integer))
        b_is_int = isinstance(b, (int, sympy.Integer))
        not_both_zero = (a != 0 or b != 0)
        h1_ok = bool(a_is_int and b_is_int and not_both_zero)
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion fails.
    # Conclusion: d divides both a and b if and only if d divides gcd(a, b)
    # We define "x divides y" as y / x being an integer.
    try:
        def divides(x, y):
            if x == 0:
                return y == 0
            # Use sympy to handle exact division for rationals, floats, etc.
            quotient = sympy.sympify(y) / sympy.sympify(x)
            return quotient.is_integer

        d_div_a = divides(d, a)
        d_div_b = divides(d, b)
        
        # Calculate gcd(a, b)
        # math.gcd handles standard integers
        g = math.gcd(int(a), int(b))
        
        d_div_g = divides(d, g)
        
        # The conclusion is (d_div_a and d_div_b) == d_div_g
        # neg_Q is True if the conclusion is False
        conclusion = (d_div_a and d_div_b) == d_div_g
        neg_q_ok = not conclusion
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a and b are integers, not both zero",
    "¬Q: It is NOT the case that (d divides both a and b iff d divides gcd(a, b))"
]

N_HYP = 1
NEG_Q_INDEX = 1