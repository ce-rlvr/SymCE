import sympy
from sympy import Symbol, simplify, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is an n x n matrix with entries in F",
    "¬Q: c_{n-1} = -Tr(A) and c_0 = (-1)^n det(A) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # H_1: F is a field
    # We verify this by checking that the entries of the matrix are commutative,
    # which is consistent with them belonging to a field.
    try:
        h1 = True
        if isinstance(witness, sympy.MatrixBase):
            for val in witness:
                if val.is_commutative is False:
                    h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: A is an n x n matrix with entries in F
    try:
        h2 = isinstance(witness, sympy.MatrixBase) and witness.is_square
    except Exception:
        h2 = False

    # neg_Q: Conclusion fails
    try:
        if not (isinstance(witness, sympy.MatrixBase) and witness.is_square):
            neg_q = False
        else:
            n = witness.rows
            if n == 0:
                # For a 0x0 matrix, the characteristic polynomial is 1 (degree 0).
                # There is no c_{n-1} (i.e., c_{-1}) coefficient.
                # Thus, the statement c_{n-1} = -Tr(A) is undefined / fails.
                neg_q = True
            else:
                x = Symbol('x')
                p = witness.charpoly(x)
                coeffs = p.all_coeffs()
                
                c_n_minus_1 = coeffs[1]
                c_0 = coeffs[-1]
                
                tr = witness.trace()
                dt = witness.det()
                
                diff1 = simplify(c_n_minus_1 + tr)
                diff2 = simplify(c_0 - ((-1)**n * dt))
                
                eq1 = (diff1 == 0) or (diff1.is_zero is True)
                eq2 = (diff2 == 0) or (diff2.is_zero is True)
                
                neg_q = not (eq1 and eq2)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]