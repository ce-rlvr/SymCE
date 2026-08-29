import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        # The witness can be provided as a tuple (R, x) or just the element x.
        if isinstance(witness, tuple) and len(witness) == 2:
            R, val = witness
        else:
            val = witness

        # H_1: x is an element of R
        # We accept standard numeric types, SymPy expressions, and matrices as valid ring elements.
        h1 = isinstance(val, (int, float, sympy.Basic)) or (hasattr(val, 'is_Matrix') and val.is_Matrix)

        # Evaluate whether the element is clean in its natural ring.
        # A clean element can be written as e + u, where e is idempotent (e^2 = e) and u is a unit.
        if isinstance(val, (int, sympy.Integer)):
            # In Z, idempotents are {0, 1} and units are {-1, 1}.
            # Clean elements are 0 + (-1) = -1, 0 + 1 = 1, 1 + (-1) = 0, 1 + 1 = 2.
            is_clean = val in [-1, 0, 1, 2]
        elif isinstance(val, float):
            # In R (a field), all elements are clean.
            is_clean = True
        elif isinstance(val, sympy.Expr):
            if val.is_number:
                if val.is_Integer:
                    is_clean = val in [-1, 0, 1, 2]
                elif val.is_Rational:
                    # In Q (a field), all elements are clean.
                    is_clean = True
                else:
                    # Assume clean for other numeric fields (R, C)
                    is_clean = True
            else:
                # In polynomial rings like Z[x] or Q[x], idempotents are {0, 1} and units are constants.
                # Thus, non-constant polynomials are not clean.
                is_clean = False
        else:
            # For matrices or other complex objects, we conservatively assume they might be clean
            # to avoid false positives in counterexample detection.
            is_clean = True

        # ¬Q: The conclusion fails (x is NOT clean)
        neg_q = not is_clean

    except Exception:
        h1 = False
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x is an element of R",
    "¬Q: x is not clean (cannot be written as idempotent + unit)"
]

N_HYP = 1
NEG_Q_INDEX = 1