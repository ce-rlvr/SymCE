import sympy
from sympy import factor_list, integer_nthroot
from sympy.abc import x, y, z, t, u, v

def is_ufd(a, b, c):
    """
    Check if the elements belong to a known Unique Factorization Domain (UFD).
    We consider ZZ, QQ, and polynomial rings over QQ as our UFDs.
    """
    if all(val.is_Integer for val in (a, b, c)):
        return True
    if all(val.is_Rational for val in (a, b, c)):
        return True
    try:
        if all(isinstance(val, sympy.Expr) and val.is_polynomial() for val in (a, b, c)):
            return True
    except Exception:
        pass
    return False

def is_unit(val):
    """
    Check if the element is a unit in its respective UFD.
    In ZZ, units are 1 and -1.
    In QQ and QQ[x], any non-zero constant is a unit.
    """
    if val.is_Integer:
        return abs(int(val)) == 1
    if val.is_Rational:
        return val != 0
    try:
        if isinstance(val, sympy.Expr):
            return val.is_constant() and val != 0
    except Exception:
        pass
    return False

def is_nth_power_up_to_unit(val, n):
    """
    Check if val can be written as u * x^n for some unit u and element x.
    """
    try:
        n = int(n)
        if n <= 0:
            return False
    except Exception:
        return False

    if val.is_Integer:
        val_int = abs(int(val))
        if val_int == 1 or val_int == 0:
            return True
        root, exact = integer_nthroot(val_int, n)
        return exact
    elif val.is_Rational:
        # In a field like QQ, every non-zero element is a unit, 
        # so a = a * 1^n is always a unit times an n-th power.
        return val != 0
    else:
        try:
            # For polynomials, we check if all exponents in the prime factorization
            # are multiples of n. The leading coefficient is extracted as a constant,
            # which is a unit in QQ[x].
            const, factors = factor_list(val)
            for base, exp in factors:
                if exp % n != 0:
                    return False
            return True
        except Exception:
            return False

def conditions(witness):
    """
    Given a witness tuple (a, b, c, n), evaluate the hypotheses and the negated conclusion.
    Returns a list of booleans: [H1, H2, H3, H4, neg_Q].
    """
    try:
        a, b, c, n = witness
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        c = sympy.sympify(c)
        n = sympy.sympify(n)
    except Exception:
        return [False] * 5

    # H_1: R is a unique factorization domain
    try:
        h1 = is_ufd(a, b, c)
    except Exception:
        h1 = False

    # H_2: a, b, and c are non-zero elements of R
    try:
        h2 = (a != 0) and (b != 0) and (c != 0)
    except Exception:
        h2 = False

    # H_3: n is a positive integer
    try:
        h3 = (n.is_Integer is True) and (int(n) > 0)
    except Exception:
        h3 = False

    # H_4: The greatest common divisor of a and b is a unit
    try:
        g = sympy.gcd(a, b)
        h4 = is_unit(g)
    except Exception:
        h4 = False

    # neg_Q: It is NOT the case that there exist units u, v and elements x, y such that a = u x^n and b = v y^n
    try:
        a_is_power = is_nth_power_up_to_unit(a, n)
        b_is_power = is_nth_power_up_to_unit(b, n)
        neg_q = not (a_is_power and b_is_power)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, and c are non-zero elements of R",
    "H_3: n is a positive integer",
    "H_4: The greatest common divisor of a and b is a unit",
    "¬Q: It is not the case that a = u x^n and b = v y^n for units u,v and elements x,y"
]

N_HYP = 4
NEG_Q_INDEX = 4