import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is a finite-dimensional algebra over k",
    "H_2: x is an element of A",
    "H_3: yx = 1 (x has a left inverse)",
    "¬Q: x is not a unit or y is not its unique two-sided inverse"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_one(val, A=None):
    try:
        if val == 1:
            return True
    except Exception:
        pass
    try:
        if hasattr(val, 'is_Identity') and val.is_Identity:
            return True
    except Exception:
        pass
    try:
        if hasattr(val, 'shape') and len(val.shape) == 2:
            if val.shape[0] == val.shape[1]:
                if val == eye(val.shape[0]):
                    return True
    except Exception:
        pass
    if A is not None:
        try:
            if hasattr(A, 'one') and val == A.one:
                return True
        except Exception:
            pass
        try:
            if hasattr(A, 'identity') and val == A.identity:
                return True
        except Exception:
            pass
    try:
        if str(val).strip() in ('1', 'I', 'Identity'):
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    A = None
    if isinstance(witness, dict):
        A = witness.get('A', None)
        x_elem = witness.get('x', None)
        y_elem = witness.get('y', None)
    elif isinstance(witness, tuple):
        if len(witness) == 4:
            k, A, x_elem, y_elem = witness
        elif len(witness) == 3:
            A, x_elem, y_elem = witness
        elif len(witness) == 2:
            x_elem, y_elem = witness
        else:
            return [False, False, False, False]
    else:
        return [False, False, False, False]

    # H1: A is a finite-dimensional algebra over k
    try:
        h1 = True
        if A is not None:
            if hasattr(A, 'is_finite_dimensional') and not A.is_finite_dimensional:
                h1 = False
        
        # If x and y are matrices, they must be square and of the same size to belong to the same algebra
        if hasattr(x_elem, 'shape') and hasattr(y_elem, 'shape'):
            if len(x_elem.shape) == 2 and len(y_elem.shape) == 2:
                if x_elem.shape[0] != x_elem.shape[1] or y_elem.shape[0] != y_elem.shape[1] or x_elem.shape != y_elem.shape:
                    h1 = False
    except Exception:
        h1 = False

    # H2: x is an element of A
    try:
        h2 = True
        if A is not None and hasattr(A, '__contains__'):
            try:
                if x_elem not in A:
                    h2 = False
            except Exception:
                pass
    except Exception:
        h2 = False

    # H3: yx = 1
    try:
        yx = y_elem * x_elem
        h3 = is_one(yx, A)
    except Exception:
        h3 = False

    # ¬Q: x is not a unit or y is not its unique two-sided inverse
    try:
        xy = x_elem * y_elem
        q = is_one(xy, A)
        neg_q = not q
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]