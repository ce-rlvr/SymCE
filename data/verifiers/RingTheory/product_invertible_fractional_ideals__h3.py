import sympy
from sympy import S
from sympy import gcd
from functools import reduce

# Top-level setup
ZZ = S.Integers
QQ = S.Rationals

def get_generator(X):
    if isinstance(X, str):
        X = X.replace(' ', '')
        if X.endswith('ZZ'):
            X = X[:-2]
            if X == '' or X == '+': return S.One
            if X == '-': return S.NegativeOne
        elif X.endswith('Z'):
            X = X[:-1]
            if X == '' or X == '+': return S.One
            if X == '-': return S.NegativeOne
    if isinstance(X, (set, list, tuple)):
        if len(X) == 0:
            return S.Zero
        if len(X) == 1:
            return sympy.Rational(list(X)[0])
        if all(isinstance(x, (int, sympy.Integer)) for x in X):
            return reduce(gcd, [sympy.Rational(x) for x in X])
        raise ValueError("Multiple generators not supported for fractional ideals")
    return sympy.Rational(X)

def is_fractional_ideal_Z(X):
    if X in ('Q', 'QQ', S.Rationals, QQ):
        return False
    try:
        get_generator(X)
        return True
    except Exception:
        return False

def is_invertible_Z(X):
    if not is_fractional_ideal_Z(X):
        return False
    try:
        q = get_generator(X)
        return q != 0
    except Exception:
        return False

def inverse_Z(X):
    if is_invertible_Z(X):
        return 1 / get_generator(X)
    return None

def multiply_ideals_Z(X, Y):
    is_Q_X = X in ('Q', 'QQ', S.Rationals, QQ)
    is_Q_Y = Y in ('Q', 'QQ', S.Rationals, QQ)
    
    if is_Q_X and is_Q_Y:
        return QQ
    if is_Q_X and is_fractional_ideal_Z(Y):
        if get_generator(Y) == 0:
            return S.Zero
        return QQ
    if is_Q_Y and is_fractional_ideal_Z(X):
        if get_generator(X) == 0:
            return S.Zero
        return QQ
        
    if is_fractional_ideal_Z(X) and is_fractional_ideal_Z(Y):
        return get_generator(X) * get_generator(Y)
    
    raise ValueError("Invalid ideals for multiplication")

def conditions(witness):
    try:
        R = witness.get('R')
        K = witness.get('K')
        I = witness.get('I')
        J = witness.get('J')
    except Exception:
        return [False, False, False, False]
    
    # H1: R is an integral domain
    try:
        h1 = R in ('Z', 'ZZ', S.Integers, 'Integers', ZZ)
    except Exception:
        h1 = False

    # H2: K is the field of fractions of R
    try:
        h2 = K in ('Q', 'QQ', S.Rationals, 'Rationals', QQ)
    except Exception:
        h2 = False

    # H3: J is a non-zero invertible fractional ideal of R
    try:
        h3 = is_fractional_ideal_Z(J) and get_generator(J) != 0 and is_invertible_Z(J)
    except Exception:
        h3 = False

    # neg_Q: The product ideal IJ is an invertible fractional ideal, and its inverse is the product of the inverses of I and J.
    try:
        valid_I = is_fractional_ideal_Z(I) or I in ('Q', 'QQ', S.Rationals, QQ)
        if not valid_I:
            neg_q = False
        else:
            IJ = multiply_ideals_Z(I, J)
            if not is_invertible_Z(IJ):
                conclusion_holds = False
            else:
                inv_IJ = inverse_Z(IJ)
                inv_I = inverse_Z(I)
                inv_J = inverse_Z(J)
                if inv_I is None or inv_J is None:
                    conclusion_holds = False
                else:
                    conclusion_holds = (abs(inv_IJ) == abs(inv_I * inv_J))
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: J is a non-zero invertible fractional ideal of R",
    "¬Q: The product ideal IJ is not an invertible fractional ideal, or its inverse is not the product of the inverses of I and J"
]

N_HYP = 3
NEG_Q_INDEX = 3