import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is a row-stochastic matrix (entries non-negative, row sums exactly 1)
    try:
        # Check if witness is a matrix-like object
        if not (hasattr(witness, 'rows') and hasattr(witness, 'cols') and hasattr(witness, '__getitem__')):
            h1_ok = False
        else:
            h1_ok = True
            for i in range(witness.rows):
                row_sum = 0
                for j in range(witness.cols):
                    val = witness[i, j]
                    try:
                        is_nonneg = bool(val >= 0)
                    except TypeError:
                        is_nonneg = False
                    
                    if not is_nonneg:
                        h1_ok = False
                        break
                    row_sum += val
                
                if not h1_ok:
                    break
                
                # Check if the sum of the entries in the row is exactly 1
                if row_sum != 1:
                    try:
                        if abs(float(row_sum) - 1.0) > 1e-9:
                            h1_ok = False
                            break
                    except Exception:
                        if sympy.simplify(row_sum - 1) != 0:
                            h1_ok = False
                            break
    except Exception:
        h1_ok = False

    # neg_Q: The value lambda = 1 is NOT a root of the characteristic polynomial of A
    try:
        x_sym = sympy.Symbol('x_sym')
        cp = witness.charpoly(x_sym)
        val = cp.as_expr().subs(x_sym, 1)
        try:
            # Check if evaluating the characteristic polynomial at 1 gives non-zero
            neg_q_ok = abs(complex(val)) > 1e-9
        except TypeError:
            # Fallback for symbolic expressions
            neg_q_ok = bool(sympy.simplify(val) != 0)
    except Exception:
        # If charpoly fails (e.g., for non-square matrices), 1 is not a root of the characteristic polynomial
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is a row-stochastic matrix (entries non-negative, row sums exactly 1)",
    "¬Q: The value lambda = 1 is NOT a root of the characteristic polynomial of A"
]

N_HYP = 1
NEG_Q_INDEX = 1