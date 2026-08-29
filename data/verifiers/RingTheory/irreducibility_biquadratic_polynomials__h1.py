import sympy
from sympy import *

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion
    of the conjecture.
    
    The witness can be provided as:
      - A tuple (n, a, b) representing the ring Z_n and elements a, b.
      - A tuple (K, a, b) where K is a sympy domain like Zmod(n).
      - A tuple (a, b) representing elements in Q.
      - A sympy Poly object.
    """
    n = None
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                K, a, b = witness
                if hasattr(K, 'mod'):
                    n = int(K.mod)
                else:
                    n = int(K)
                a = int(a)
                b = int(b)
            elif len(witness) == 2:
                a, b = witness
                a = sympy.Rational(a)
                b = sympy.Rational(b)
            else:
                return [False] * 5
        elif hasattr(witness, 'domain'):
            if hasattr(witness.domain, 'mod'):
                n = int(witness.domain.mod)
            coeffs = witness.all_coeffs()
            if len(coeffs) == 5:
                a = coeffs[2]
                b = coeffs[4]
                if n is None:
                    a = sympy.Rational(a)
                    b = sympy.Rational(b)
                else:
                    a = int(a)
                    b = int(b)
            else:
                return [False] * 5
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    def is_square(y):
        if n is not None:
            y = y % n
            for i in range(n):
                if (i * i) % n == y:
                    return True
            return False
        else:
            if y < 0: 
                return False
            y_rat = sympy.Rational(y)
            return sympy.is_square(y_rat.p) and sympy.is_square(y_rat.q)

    try:
        if n is not None:
            h1 = isinstance(n, int) and n > 1 and isinstance(a, int) and isinstance(b, int)
        else:
            h1 = isinstance(a, sympy.Rational) and isinstance(b, sympy.Rational)
    except Exception:
        h1 = False

    try:
        h2 = not is_square(b)
    except Exception:
        h2 = False

    try:
        h3 = not is_square(a**2 - 4 * b)
    except Exception:
        h3 = False

    try:
        h4 = not is_square(b * (a**2 - 4 * b))
    except Exception:
        h4 = False

    try:
        if n is not None:
            reducible = False
            # Check for a linear factor (root in Z_n)
            for x in range(n):
                if (x**4 + a*x**2 + b) % n == 0:
                    reducible = True
                    break
            
            # Check for quadratic factors in Z_n
            if not reducible:
                for c in range(n):
                    for d in range(n):
                        for e in range(n):
                            if (e + d - c**2) % n == a % n:
                                if (c * (e - d)) % n == 0:
                                    if (d * e) % n == b % n:
                                        reducible = True
                                        break
                        if reducible: break
                    if reducible: break
            neg_q = reducible
        else:
            # Over Q
            x = sympy.Symbol('x')
            poly = x**4 + a*x**2 + b
            factors = sympy.factor_list(poly)
            # It is reducible if there is more than one irreducible factor, 
            # or if the single irreducible factor has multiplicity > 1.
            neg_q = len(factors[1]) > 1 or factors[1][0][1] > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are elements of K",
    "H_2: b is not a square in K",
    "H_3: a^2 - 4b is not a square in K",
    "H_4: b(a^2 - 4b) is not a square in K",
    "¬Q: x^4 + a x^2 + b is reducible over K"
]

N_HYP = 4
NEG_Q_INDEX = 4