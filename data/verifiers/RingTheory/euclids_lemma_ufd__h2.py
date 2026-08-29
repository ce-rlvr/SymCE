import sympy
import sympy.polys
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ

def divides(R, x_val, y_val):
    """Check if x_val divides y_val in the ring R."""
    zero = getattr(R, 'zero', 0)
    
    # Handle division by zero
    try:
        if x_val == zero or x_val == 0:
            return y_val == zero or y_val == 0
    except Exception:
        pass

    # Try exact quotient in the domain
    try:
        R.exquo(y_val, x_val)
        return True
    except Exception:
        pass

    # Try remainder in the domain
    try:
        return R.rem(y_val, x_val) == zero
    except Exception:
        pass

    # Fallback to standard modulo
    try:
        return y_val % x_val == 0
    except Exception:
        pass

    # Fallback to divmod
    try:
        q, r = divmod(y_val, x_val)
        return r == 0 or r == zero
    except Exception:
        pass

    return False

def is_coprime(R, a, b):
    """Check if the greatest common divisor of a and b is a unit in R."""
    one = getattr(R, 'one', 1)
    zero = getattr(R, 'zero', 0)
    
    g = None
    try:
        g = R.gcd(a, b)
    except Exception:
        try:
            g = sympy.gcd(a, b)
        except Exception:
            pass

    if g is None:
        return False

    # Check if g is a unit
    try:
        if hasattr(R, 'is_unit'):
            return R.is_unit(g)
    except Exception:
        pass

    try:
        R.exquo(one, g)
        return True
    except Exception:
        pass

    try:
        return R.rem(one, g) == zero
    except Exception:
        pass

    try:
        return 1 % g == 0
    except Exception:
        pass

    try:
        return g == 1 or g == -1 or g == one or g == -one
    except Exception:
        pass

    return False

def conditions(witness) -> list[bool]:
    # Unpack the witness
    try:
        if hasattr(witness, '__len__'):
            if len(witness) == 4:
                R, a, b, c = witness
            elif len(witness) == 3:
                a_sym, b_sym, c_sym = witness
                try:
                    # Infer the domain if not explicitly provided
                    R, (a, b, c) = sympy.polys.construct_domain([a_sym, b_sym, c_sym])
                except Exception:
                    R = sympy.ZZ
                    a, b, c = a_sym, b_sym, c_sym
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a unique factorization domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False

    # H_2: a divides the product bc
    try:
        try:
            bc = R.mul(b, c)
        except Exception:
            bc = b * c
        h2 = bool(divides(R, a, bc))
    except Exception:
        h2 = False

    # H_3: a and b are coprime (their greatest common divisor is a unit)
    try:
        h3 = bool(is_coprime(R, a, b))
    except Exception:
        h3 = False

    # ¬Q: a does not divide c
    try:
        neg_q = not bool(divides(R, a, c))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a divides the product bc",
    "H_3: a and b are coprime (their greatest common divisor is a unit)",
    "¬Q: a does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3