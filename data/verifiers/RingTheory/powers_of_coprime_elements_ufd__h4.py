import sympy
import math

x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            n = witness.get('n')
        else:
            a, b, c, n = witness
            
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        c = sympy.sympify(c)
        n = int(n)
    except Exception:
        return [False, False, False, False, False]

    try:
        h1 = True
    except Exception:
        h1 = False

    try:
        h2 = bool(a != 0 and b != 0 and c != 0)
    except Exception:
        h2 = False

    try:
        g = sympy.gcd(a, b)
        if g.is_Integer or g.is_Rational:
            h3 = bool(abs(g) == 1)
        else:
            poly = g.as_poly()
            h3 = bool(poly is not None and poly.degree() == 0)
    except Exception:
        h3 = False

    try:
        h4 = bool(sympy.expand(a * b) == sympy.expand(c**n))
    except Exception:
        h4 = False

    try:
        def is_nth_power(val, p_n):
            if val.is_Integer or val.is_Rational:
                if p_n <= 0:
                    return abs(val) == 1
                factors = sympy.factorint(abs(val))
                return all(m % p_n == 0 for p, m in factors.items())
            else:
                if p_n <= 0:
                    poly = val.as_poly()
                    return poly is not None and poly.degree() == 0
                const, factors = sympy.factor_list(val)
                return all(m % p_n == 0 for f, m in factors)

        neg_q = not (is_nth_power(a, n) and is_nth_power(b, n))
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, c are non-zero elements of R",
    "H_3: a and b are relatively prime",
    "H_4: ab = c^n",
    "¬Q: a and b are not both n-th powers up to a unit"
]

N_HYP = 4
NEG_Q_INDEX = 4