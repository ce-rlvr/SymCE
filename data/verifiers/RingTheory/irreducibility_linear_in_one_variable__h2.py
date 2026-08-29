import sympy
from sympy import gcd, Poly
from sympy.abc import x, y

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    
    The witness should be a tuple: (R_is_UFD, a, b)
    where:
      - R_is_UFD is a boolean (or a function returning a boolean) indicating if R is a UFD.
      - a and b are sympy expressions representing a(x) and b(x).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R_is_UFD, a, b = witness
                h1 = bool(R_is_UFD() if callable(R_is_UFD) else R_is_UFD)
            elif len(witness) == 2:
                a, b = witness
                h1 = True
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        # a(x) and b(x) must be polynomials in x, so they shouldn't contain y
        if (hasattr(a, 'free_symbols') and y in a.free_symbols) or \
           (hasattr(b, 'free_symbols') and y in b.free_symbols):
            return [False, False, False, False]
    except Exception:
        pass

    try:
        a_poly = Poly(a, x)
        h2 = not a_poly.is_zero
    except Exception:
        h2 = False

    try:
        g = gcd(a, b)
        h3 = (g == 1 or g == -1)
    except Exception:
        h3 = False

    try:
        f = a * y + b
        factors = sympy.factor_list(f)
        content = abs(factors[0])
        num_factors = sum(power for factor, power in factors[1])
        # A polynomial is reducible if it can be factored into two non-units.
        # In sympy's factor_list over Z, a constant factor > 1 is a non-unit.
        # Multiple polynomial factors also mean it's reducible.
        neg_q = (content > 1 and num_factors >= 1) or (num_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a UFD",
    "H_2: a(x) is not the zero polynomial",
    "H_3: gcd of a(x) and b(x) is 1",
    "not Q: a(x)y + b(x) is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3