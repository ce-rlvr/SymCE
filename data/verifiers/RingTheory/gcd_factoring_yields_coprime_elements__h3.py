import sympy
from sympy import sympify, cancel, fraction, gcd
from sympy.abc import x, y, z
from sympy import Rational, Integer

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide elements a, b, and d of a UFD.
    It can be a tuple (a, b, d), a tuple (R, a, b, d), or a dict {'a': a, 'b': b, 'd': d}.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            d = witness.get('d')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                a, b, d = witness
            elif len(witness) == 4:
                _, a, b, d = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        if a is None or b is None or d is None:
            return [False, False, False]

        a = sympify(a)
        b = sympify(b)
        d = sympify(d)

        # H_1: R is a unique factorization domain
        # We accept any valid sympy expression, as Z, Z[i], and polynomial rings over fields are UFDs.
        h1 = True

        # H_2: a and b are non-zero elements of R
        h2 = (a != 0) and (b != 0)

        # ¬Q: The greatest common divisor of a/d and b/d is not a unit in R
        if d == 0:
            neg_q = True
        else:
            ad = cancel(a / d)
            bd = cancel(b / d)
            
            if fraction(ad)[1] != 1 or fraction(bd)[1] != 1:
                # d does not divide a or b in the ring, so a/d or b/d is not in R
                neg_q = True
            else:
                g = gcd(ad, bd)
                # In Z, Z[i], and Z[x], the units have an absolute value of 1.
                # If g is a polynomial, abs(g) will be a symbolic Abs, which evaluates to != 1.
                neg_q = (abs(g) != 1)

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a and b are non-zero elements of R",
    "¬Q: The greatest common divisor of a/d and b/d is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2