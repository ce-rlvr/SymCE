import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: 1 - ab is a unit in R",
    "¬Q: 1 - ba is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Parse the witness
    if isinstance(witness, dict):
        if 'a' in witness and 'b' in witness:
            a = witness['a']
            b = witness['b']
            R = witness.get('R', None)
        else:
            return [False, False, False]
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            R, a, b = witness
        elif len(witness) == 2:
            a, b = witness
            R = None
        else:
            return [False, False, False]
    else:
        return [False, False, False]

    # Convert lists/tuples to sympy Matrices if applicable
    if isinstance(a, (list, tuple)):
        try:
            a = sympy.Matrix(a)
        except Exception:
            pass
    if isinstance(b, (list, tuple)):
        try:
            b = sympy.Matrix(b)
        except Exception:
            pass

    # Precompute ab
    try:
        ab = a * b
    except Exception:
        return [False, False, False]

    # H_1: R is a ring with identity
    h1 = False
    try:
        if hasattr(a, 'rows') and hasattr(b, 'rows'):
            # For matrices, the ring R is the set of square matrices of size ab.rows
            h1 = (ab.rows == ab.cols)
        else:
            # Scalars belong to a ring with identity
            h1 = True
    except Exception:
        h1 = False

    # H_2: 1 - ab is a unit in R
    h2 = False
    try:
        if hasattr(a, 'rows') and hasattr(b, 'rows'):
            n = ab.rows
            I_n = sympy.eye(n)
            u = I_n - ab
            # Check if u is invertible
            _ = u.inv()
            h2 = True
        else:
            u = 1 - ab
            if R is not None and hasattr(R, 'is_unit'):
                h2 = R.is_unit(u)
            elif isinstance(u, sympy.Mod):
                val, mod = u.args
                h2 = (sympy.gcd(val, mod) == 1)
            elif isinstance(u, (sympy.Integer, int)):
                h2 = (u == 1 or u == -1)
            else:
                h2 = (u != 0)
    except Exception:
        h2 = False

    # ¬Q: 1 - ba is not a unit in R
    q = False
    try:
        if hasattr(a, 'rows') and hasattr(b, 'rows'):
            n = ab.rows
            ba = b * a
            # To be a unit in R, 1 - ba must first be an element of R.
            # R is the ring of n x n matrices. If ba is not n x n, it's not in R.
            if ba.rows != n or ba.cols != n:
                q = False
            else:
                I_n = sympy.eye(n)
                v = I_n - ba
                _ = v.inv()
                q = True
        else:
            ba = b * a
            v = 1 - ba
            if R is not None and hasattr(R, 'is_unit'):
                q = R.is_unit(v)
            elif isinstance(v, sympy.Mod):
                val, mod = v.args
                q = (sympy.gcd(val, mod) == 1)
            elif isinstance(v, (sympy.Integer, int)):
                q = (v == 1 or v == -1)
            else:
                q = (v != 0)
    except Exception:
        q = False

    return [h1, h2, not q]