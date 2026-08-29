import sympy
from sympy.matrices import MatrixBase, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: For all integers i from 1 to n-1, the product a_{i,i+1} a_{i+1,i} > 0
    try:
        if not (isinstance(witness, MatrixBase) and witness.rows == witness.cols and witness.rows > 0):
            h1 = False
        else:
            n = witness.rows
            h1 = True
            for i in range(n - 1):
                prod = witness[i, i+1] * witness[i+1, i]
                try:
                    if float(prod) <= 0:
                        h1 = False
                        break
                except TypeError:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # neg_Q: A is not diagonalizable over the real numbers
    try:
        if not (isinstance(witness, MatrixBase) and witness.rows == witness.cols and witness.rows > 0):
            neg_q = False
        else:
            n = witness.rows
            eigenvects = witness.eigenvects()
            is_diag = True
            geom_sum = 0
            for val, mult, basis in eigenvects:
                is_real = False
                if val.is_real is True:
                    is_real = True
                elif val.is_real is False:
                    is_real = False
                else:
                    try:
                        float(val)
                        is_real = True
                    except TypeError:
                        c = val.evalf()
                        if hasattr(c, 'as_real_imag'):
                            re, im = c.as_real_imag()
                            if abs(float(im)) <= 1e-9:
                                is_real = True
                
                if not is_real:
                    is_diag = False
                    break
                geom_sum += len(basis)
            
            if geom_sum != n:
                is_diag = False
                
            neg_q = not is_diag
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: For all integers i from 1 to n-1, the product a_{i,i+1} a_{i+1,i} > 0",
    "¬Q: A is not diagonalizable over the real numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1