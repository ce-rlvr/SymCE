import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals
RR = sympy.S.Reals
CC = sympy.S.Complexes

def is_integral_domain(R):
    if R in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
        return True
    try:
        from sympy.polys.domains import ZZ as polyZZ, QQ as polyQQ, RR as polyRR, CC as polyCC
        if R in (polyZZ, polyQQ, polyRR, polyCC):
            return True
    except Exception:
        pass
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    if hasattr(R, 'is_IntegralDomain') and R.is_IntegralDomain:
        return True
    if str(R) in ('ZZ', 'QQ', 'RR', 'CC', 'Integers', 'Rationals', 'Reals', 'Complexes'):
        return True
    return False

def is_zero(val):
    if hasattr(val, 'is_zero_matrix') and val.is_zero_matrix:
        return True
    if hasattr(val, 'is_zero') and val.is_zero:
        return True
    if val == 0:
        return True
    try:
        if bool(val == 0):
            return True
    except Exception:
        pass
    return False

def is_equal(val1, val2):
    if val1 == val2:
        return True
    try:
        if bool(val1 == val2):
            return True
    except Exception:
        pass
    try:
        if hasattr(val1 - val2, 'is_zero_matrix') and (val1 - val2).is_zero_matrix:
            return True
    except Exception:
        pass
    try:
        diff = sympy.simplify(val1 - val2)
        if diff == 0:
            return True
        if hasattr(diff, 'is_zero') and diff.is_zero:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # Extract R, a, b, c from the witness
    if isinstance(witness, dict):
        R = witness.get('R', sympy.S.Integers)
        a = witness.get('a')
        b = witness.get('b')
        c = witness.get('c')
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 4:
            R, a, b, c = witness
        elif len(witness) == 3:
            R = sympy.S.Integers
            a, b, c = witness
        else:
            return [False, False, False, False]
    else:
        return [False, False, False, False]

    # H_1: R is an integral domain
    try:
        h1 = is_integral_domain(R)
    except Exception:
        h1 = False

    # H_2: a is not equal to 0
    try:
        h2 = not is_zero(a)
    except Exception:
        h2 = False

    # H_3: ab = ac
    try:
        ab = a * b
        ac = a * c
        h3 = is_equal(ab, ac)
    except Exception:
        h3 = False

    # ¬Q: b is not equal to c
    try:
        neg_q = not is_equal(b, c)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: a is not equal to 0",
    "H_3: ab = ac",
    "¬Q: b is not equal to c"
]

N_HYP = 3
NEG_Q_INDEX = 3