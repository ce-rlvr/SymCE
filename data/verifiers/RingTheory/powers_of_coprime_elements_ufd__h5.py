import sympy as sp
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, c are non-zero elements of R",
    "H_3: a and b are relatively prime",
    "H_4: n >= 2 is an integer",
    "¬Q: a is not of the form u x^n or b is not of the form v y^n"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False] * 5
        a, b, c, n = witness
    except Exception:
        return [False] * 5

    # H_1: R is a unique factorization domain
    # We verify that the elements belong to ZZ or a polynomial ring over QQ/ZZ, which are UFDs.
    try:
        def is_valid_element(val):
            if isinstance(val, (int, sp.Integer)):
                return True
            if isinstance(val, sp.Expr) and not val.has(sp.Float):
                return True
            return False
        h1 = is_valid_element(a) and is_valid_element(b) and is_valid_element(c)
    except Exception:
        h1 = False

    # H_2: a, b, c are non-zero elements of R
    try:
        h2 = (a != 0) and (b != 0) and (c != 0)
    except Exception:
        h2 = False

    # H_3: a and b are relatively prime
    try:
        gcd_ab = sp.gcd(a, b)
        # In a UFD, the GCD being a unit means its prime factorization has no prime factors.
        _, factors = sp.factor_list(gcd_ab)
        h3 = (len(factors) == 0)
    except Exception:
        h3 = False

    # H_4: n >= 2 is an integer
    try:
        h4 = isinstance(n, (int, sp.Integer)) and int(n) >= 2
    except Exception:
        h4 = False

    # ¬Q: a is not of the form u x^n or b is not of the form v y^n
    try:
        def is_unit_times_nth_power(val, power):
            # If val = u * x^n, then in its prime factorization all exponents must be multiples of n.
            _, factors = sp.factor_list(val)
            return all(e % power == 0 for _, e in factors)
        
        a_is_power = is_unit_times_nth_power(a, n)
        b_is_power = is_unit_times_nth_power(b, n)
        
        neg_q = not (a_is_power and b_is_power)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]