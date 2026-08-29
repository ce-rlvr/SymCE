import sympy
from sympy import Matrix, eye, zeros
import z3

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_xy(witness):
    """Extract x and y from the witness object."""
    if isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            return witness[0], witness[1]
        elif len(witness) >= 3:
            return witness[1], witness[2]
    elif isinstance(witness, dict):
        if 'x' in witness and 'y' in witness:
            return witness['x'], witness['y']
    return None, None

def conditions(witness) -> list[bool]:
    # H_1: R is a ring
    h1_ok = False
    try:
        x, y = get_xy(witness)
        if x is not None and y is not None:
            if hasattr(x, 'is_Matrix') and x.is_Matrix:
                h1_ok = (x.shape[0] == x.shape[1])
            else:
                h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: x and y are elements of R
    h2_ok = False
    try:
        x, y = get_xy(witness)
        if x is not None and y is not None:
            # Check if they support ring operations
            _ = x + y
            _ = x * y
            _ = y * x
            _ = x - y
            if hasattr(x, 'is_Matrix') and x.is_Matrix:
                h2_ok = (x.shape == y.shape)
            else:
                h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: yx is not a nilpotent element
    neg_q_ok = False
    try:
        x, y = get_xy(witness)
        if x is not None and y is not None:
            yx = y * x
            if hasattr(yx, 'is_Matrix') and yx.is_Matrix:
                n = yx.shape[0]
                if n == 0:
                    is_nilp = True
                else:
                    is_nilp = bool(yx**n == yx.__class__.zeros(n, n))
            elif type(yx).__module__.startswith('z3'):
                solver = z3.Solver()
                solver.add(yx != 0)
                is_nilp = (solver.check() == z3.unsat)
            else:
                from sympy import simplify
                is_nilp = bool(simplify(yx) == 0)
            
            neg_q_ok = not is_nilp
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: x and y are elements of R",
    "¬Q: yx is not a nilpotent element"
]

N_HYP = 2
NEG_Q_INDEX = 2