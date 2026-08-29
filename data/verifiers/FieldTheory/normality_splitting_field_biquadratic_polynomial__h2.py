import math
import sympy
from sympy import Rational

# Top-level setup for potential witness expressions
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness can be a tuple (a, b) assuming characteristic 0,
    a tuple (char, a, b) for a specific field characteristic,
    or a dictionary with keys 'a', 'b', and optionally 'char'.
    """
    try:
        if isinstance(witness, dict):
            char = witness.get('char', 0)
            a = witness.get('a')
            b = witness.get('b')
            if a is None or b is None:
                return [False, False, False]
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                char = 0
                a, b = witness
            elif len(witness) == 3:
                char, a, b = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: F is a field of characteristic not equal to 2
    try:
        if char != 0 and not sympy.isprime(char):
            h1 = False
        else:
            h1 = (char != 2)
            
        # Verify a and b are valid elements in the field
        if char == 0:
            Rational(a)
            Rational(b)
        else:
            int(a)
            int(b)
    except Exception:
        h1 = False

    # H_2: E is the splitting field of the polynomial (x^2 - a)(x^2 - b) over F
    # This is true by definition for any valid a, b in F.
    h2 = h1

    # ¬Q: E is not a normal extension of degree 4, or its automorphism group is not V4
    # For a biquadratic polynomial, the extension is normal. The degree is 4 (and Aut is V4)
    # if and only if a, b, and a*b are all non-squares in F.
    try:
        if not h1:
            neg_q = False
        else:
            def is_square(val, c):
                if c == 0:
                    if val < 0:
                        return False
                    r = Rational(val)
                    num, den = r.p, r.q
                    return math.isqrt(num)**2 == num and math.isqrt(den)**2 == den
                else:
                    v = int(val) % c
                    if v == 0:
                        return True
                    # Euler's criterion for odd primes
                    return pow(v, (c - 1) // 2, c) == 1

            sa = is_square(a, char)
            sb = is_square(b, char)
            if char > 0:
                sab = is_square((int(a) % char) * (int(b) % char), char)
            else:
                sab = is_square(a * b, char)
            
            degree_is_4 = (not sa) and (not sb) and (not sab)
            neg_q = not degree_is_4
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: E is the splitting field of the polynomial (x^2 - a)(x^2 - b) over F",
    "¬Q: E is not a normal extension of degree 4, or its automorphism group is not V4"
]

N_HYP = 2
NEG_Q_INDEX = 2