import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Attempt to convert to a sympy Matrix if it isn't already
    try:
        if not isinstance(witness, sp.MatrixBase):
            witness = sp.Matrix(witness)
    except Exception:
        pass

    # H_1: A is an n x n invertible matrix over C
    try:
        h1 = False
        if isinstance(witness, sp.MatrixBase) and witness.is_square:
            det = sp.simplify(witness.det())
            if det != 0:
                h1 = True
    except Exception:
        h1 = False

    # Q: The singular values of A^-1 are 1/sigma_n >= 1/sigma_{n-1} >= ... >= 1/sigma_1
    neg_q = False
    try:
        if h1:
            sv_A = witness.singular_values()
            sv_Ainv = witness.inv().singular_values()
            n = len(sv_A)
            q = True
            for i in range(n):
                # sv_Ainv is sorted descending.
                # sv_A is sorted descending, so 1 / sv_A[n - 1 - i] is the expected i-th largest singular value of A^-1.
                val1 = sv_Ainv[i]
                val2 = 1 / sv_A[n - 1 - i]
                
                diff = sp.simplify(val1 - val2)
                if diff == 0:
                    continue
                if hasattr(diff, 'is_zero') and diff.is_zero:
                    continue
                
                try:
                    c_diff = complex(diff)
                except Exception:
                    # If the difference contains symbols and didn't simplify to 0, we cannot be sure.
                    raise ValueError("Cannot evaluate symbolic difference")
                
                if abs(c_diff) < 1e-9:
                    continue
                
                q = False
                break
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n invertible matrix over C",
    "¬Q: The singular values of A^-1 are not 1/sigma_n >= 1/sigma_{n-1} >= ... >= 1/sigma_1"
]

N_HYP = 1
NEG_Q_INDEX = 1