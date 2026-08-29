import sympy
import math

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    # H_1: Let U be an n x n matrix over the complex numbers
    try:
        h1 = isinstance(witness, sympy.matrices.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # H_2: Let p(x) be the characteristic polynomial of U
    try:
        if h1:
            p = witness.charpoly()
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: Not every root of p(x) has an absolute value equal to 1
    try:
        if h1 and h2:
            all_one = True
            try:
                p = witness.charpoly()
                roots = p.nroots()
                for r in roots:
                    if abs(abs(complex(r)) - 1.0) > 1e-7:
                        all_one = False
                        break
            except Exception:
                # Fallback to symbolic eigenvalues if nroots fails (e.g., symbolic matrix)
                roots = witness.eigenvals().keys()
                for r in roots:
                    diff = sympy.simplify(sympy.Abs(r) - 1)
                    if diff == 0:
                        continue
                    try:
                        num_val = sympy.Abs(r).evalf()
                        if abs(float(num_val) - 1.0) < 1e-7:
                            continue
                    except Exception:
                        pass
                    all_one = False
                    break
            neg_q = not all_one
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n matrix over the complex numbers",
    "H_2: p(x) is the characteristic polynomial of U",
    "¬Q: Not every root of p(x) has an absolute value equal to 1"
]

N_HYP = 2
NEG_Q_INDEX = 2