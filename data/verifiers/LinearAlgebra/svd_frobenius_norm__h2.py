import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    # H_1: A is an m x n complex matrix.
    try:
        if not isinstance(witness, sp.MatrixBase):
            h1 = False
        else:
            h1 = True
            for val in witness:
                # If a value is explicitly known to not be complex, it fails the hypothesis.
                if val.is_complex is False:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # ¬Q: The square of the Frobenius norm of A is NOT equal to the sum of the squares of its singular values.
    try:
        m, n = witness.shape
        
        # Compute the square of the Frobenius norm
        frob_sq = sum(sp.Abs(x)**2 for x in witness)
        
        # Compute the sum of the squares of the singular values
        sv = witness.singular_values()
        sv_sq_sum = sum(s**2 for s in sv)
        
        # Check if they are equal
        diff = sp.simplify(frob_sq - sv_sq_sum)
        
        if diff == 0:
            neg_q = False
        else:
            try:
                # Attempt numerical evaluation for constant expressions
                val = complex(diff.evalf())
                neg_q = abs(val) > 1e-9
            except Exception:
                try:
                    # Fallback to symbolic equivalence check
                    is_zero = diff.equals(0)
                    if is_zero is True:
                        neg_q = False
                    else:
                        neg_q = True
                except Exception:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "¬Q: The square of the Frobenius norm of A is not equal to the sum of the squares of its singular values"
]

N_HYP = 1
NEG_Q_INDEX = 1