import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_commutative_ring_with_identity(R):
    try:
        if hasattr(R, 'is_commutative'):
            if not R.is_commutative:
                return False
        if hasattr(R, 'has_identity'):
            if not R.has_identity:
                return False
        if isinstance(R, (list, tuple, set)):
            R_list = list(R)
            for i in R_list:
                for j in R_list:
                    if i * j != j * i:
                        return False
            has_id = False
            for e in R_list:
                if all(e * j == j and j * e == j for j in R_list):
                    has_id = True
                    break
            if not has_id:
                return False
            return True
        return True
    except Exception:
        return False

def get_implicit_domain(a, b):
    try:
        elements = []
        for val in (a, b):
            if isinstance(val, sympy.MatrixBase):
                elements.extend(list(val))
            elif isinstance(val, (list, tuple)):
                elements.extend(list(val))
            else:
                elements.append(val)
        
        sym_elements = []
        for e in elements:
            if isinstance(e, (int, float, complex)):
                sym_elements.append(sympy.sympify(e))
            elif isinstance(e, sympy.Expr):
                sym_elements.append(e)
                
        if sym_elements:
            domain, _ = sympy.polys.domains.construct_domain(sym_elements)
            return domain
    except Exception:
        pass
    return None

def is_in_R(val, R):
    if R is None:
        return True
    if isinstance(R, (list, tuple, set)):
        return val in R
    if hasattr(R, 'convert'):
        try:
            if isinstance(val, sympy.MatrixBase):
                for e in val:
                    R.convert(e)
                return True
            R.convert(val)
            return True
        except Exception:
            return False
    return True

def is_unit_in_R(val, R=None):
    if R is not None:
        if hasattr(R, 'is_unit') and not isinstance(val, sympy.MatrixBase):
            try:
                return bool(R.is_unit(R.convert(val)))
            except Exception:
                pass
        if isinstance(R, (list, tuple, set)):
            try:
                R_list = list(R)
                identities = [e for e in R_list if all(e * y == y and y * e == y for y in R_list)]
                if identities:
                    one = identities[0]
                    for y in R_list:
                        if val * y == one and y * val == one:
                            return True
                    return False
            except Exception:
                pass

    try:
        if isinstance(val, sympy.MatrixBase):
            if val.shape[0] != val.shape[1]:
                return False
            det = val.det()
            if det == 0:
                return False
            if R is not None and hasattr(R, 'is_unit'):
                try:
                    return bool(R.is_unit(R.convert(det)))
                except Exception:
                    pass
            if all(isinstance(e, (int, sympy.Integer)) for e in val):
                return abs(det) == 1
            return True
    except Exception:
        pass

    try:
        if hasattr(val, 'is_unit'):
            if callable(val.is_unit):
                return bool(val.is_unit())
            return bool(val.is_unit)
    except Exception:
        pass

    try:
        if isinstance(val, (int, sympy.Integer)):
            return abs(val) == 1
    except Exception:
        pass

    try:
        if isinstance(val, sympy.Expr):
            if val.is_number:
                return bool(val != 0)
    except Exception:
        pass

    try:
        if isinstance(val, float):
            return val != 0.0
    except Exception:
        pass

    try:
        if isinstance(val, complex):
            return val != 0j
    except Exception:
        pass

    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, a, b = witness
            elif len(witness) == 2:
                R = None
                a, b = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring with identity
    h1_ok = False
    try:
        if a * b != b * a:
            h1_ok = False
        elif R is not None:
            h1_ok = is_commutative_ring_with_identity(R)
        else:
            if isinstance(a, sympy.MatrixBase) and isinstance(b, sympy.MatrixBase):
                h1_ok = (a.shape[0] == 1)
            else:
                h1_ok = True
    except Exception:
        h1_ok = False

    R_implicit = R if R is not None else get_implicit_domain(a, b)

    # H2: The product ab is a unit in R
    h2_ok = False
    try:
        if R is not None:
            if not (is_in_R(a, R) and is_in_R(b, R)):
                raise ValueError("Elements not in R")
        ab = a * b
        h2_ok = is_unit_in_R(ab, R_implicit)
    except Exception:
        h2_ok = False

    # neg_Q: Both a and b are units in R (negated -> at least one is not a unit)
    neg_q_ok = False
    try:
        a_is_unit = is_unit_in_R(a, R_implicit)
        b_is_unit = is_unit_in_R(b, R_implicit)
        neg_q_ok = not (a_is_unit and b_is_unit)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: The product ab is a unit in R",
    "¬Q: At least one of a or b is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2