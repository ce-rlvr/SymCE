import sympy
from sympy import Matrix, eye, zeros, re, im

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H1: A is an n x n matrix with real entries
    try:
        if not isinstance(witness, Matrix):
            h1 = False
        elif not witness.is_square:
            h1 = False
        else:
            h1 = True
            for e in witness:
                if e.is_real is False:
                    h1 = False
                    break
                elif e.is_real is None:
                    if sympy.im(e).simplify() != 0:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # neg_Q: A is not unitarily diagonalizable over C OR its eigenvalues are not purely imaginary or zero
    try:
        if not h1:
            neg_q = False
        else:
            # A is unitarily diagonalizable over C iff it is normal
            # Since A is real, A.H == A.T
            is_normal = (witness * witness.T == witness.T * witness)
            
            evals = witness.eigenvals()
            pure_imag_or_zero = True
            for val in evals:
                real_part = sympy.re(val).simplify()
                if real_part == 0:
                    continue
                try:
                    if float(real_part) != 0.0:
                        pure_imag_or_zero = False
                        break
                except TypeError:
                    if real_part.is_zero is False:
                        pure_imag_or_zero = False
                        break
            
            neg_q = not (is_normal and pure_imag_or_zero)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with real entries",
    "¬Q: A is not unitarily diagonalizable over C, or its eigenvalues are not purely imaginary or zero"
]

N_HYP = 1
NEG_Q_INDEX = 1