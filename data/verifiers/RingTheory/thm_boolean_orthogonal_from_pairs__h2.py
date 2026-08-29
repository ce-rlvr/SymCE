import sympy
from sympy import Matrix, eye, zeros
from sympy.polys.domains import GF
from sympy.abc import t, x, y, z

# Top-level setup
Z2 = GF(2)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_witness(witness):
    if isinstance(witness, dict):
        return witness.get('R'), witness.get('x'), witness.get('y')
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            return witness
        elif len(witness) == 2:
            return None, witness[0], witness[1]
    elif hasattr(witness, 'R') and hasattr(witness, 'x') and hasattr(witness, 'y'):
        return witness.R, witness.x, witness.y
    return None, None, None

def is_boolean_ring(R):
    if R is None:
        return False
    if str(R) == 'GF(2)':
        return True
    if type(R).__name__ == 'GaloisField' and getattr(R, 'mod', None) == 2:
        return True
    if hasattr(R, 'characteristic') and R.characteristic() == 2 and hasattr(R, 'order') and R.order() == 2:
        return True
    try:
        elements = list(R)
        if not elements:
            return False
        for a in elements:
            if a * a != a:
                return False
        for a in elements:
            for b in elements:
                if (a + b) not in elements:
                    return False
                if (a * b) not in elements:
                    return False
        return True
    except Exception:
        pass
    if hasattr(R, 'is_boolean_ring'):
        if callable(R.is_boolean_ring):
            return R.is_boolean_ring()
        return R.is_boolean_ring
    return False

def is_zero(val):
    try:
        if hasattr(val, 'is_zero_matrix') and val.is_zero_matrix:
            return True
    except Exception:
        pass
    try:
        if hasattr(val, 'is_zero') and val.is_zero is True:
            return True
    except Exception:
        pass
    try:
        if val == 0:
            return True
    except Exception:
        pass
    try:
        from sympy import expand
        if expand(val) == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    R, x_val, y_val = extract_witness(witness)
    
    try:
        h1 = bool(is_boolean_ring(R))
    except Exception:
        h1 = False
        
    try:
        if x_val is None or y_val is None:
            neg_q = False
        else:
            xy = x_val * y_val
            term1 = x_val - xy
            term2 = y_val - xy
            prod = term1 * term2
            neg_q = not is_zero(prod)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: The product (x - x y)(y - x y) is not equal to 0"
]

N_HYP = 1
NEG_Q_INDEX = 1