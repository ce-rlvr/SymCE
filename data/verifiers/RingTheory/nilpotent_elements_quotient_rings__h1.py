import sympy
from sympy import Matrix, zeros, eye
from sympy.matrices import MatrixBase

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    R = None
    I = None
    x = None
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                a, b, c = witness
                if hasattr(a, 'shape') and not isinstance(a, MatrixBase):
                    R, I, x = a, b, c
                elif hasattr(b, 'shape') and not isinstance(b, MatrixBase):
                    I, R, x = a, b, c
                elif isinstance(a, str):
                    R, I, x = a, b, c
                elif isinstance(b, str):
                    I, R, x = a, b, c
                else:
                    R, I, x = a, b, c
            elif len(witness) == 2:
                I, x = witness
                if isinstance(x, MatrixBase):
                    R = "MatrixSpace"
            else:
                return [False, False, False]
        else:
            x = witness
            if isinstance(x, MatrixBase):
                R = "MatrixSpace"
                I = zeros(x.rows, x.cols)
    except Exception:
        return [False, False, False]

    # H_1: I is an ideal of R
    h1_ok = False
    try:
        if isinstance(I, MatrixBase) and I.is_zero:
            h1_ok = True
        elif isinstance(I, (list, tuple, set)) and len(I) > 0 and all(isinstance(m, MatrixBase) and m.is_zero for m in I):
            h1_ok = True
        elif I == 0:
            h1_ok = True
        elif isinstance(I, int) or hasattr(I, 'is_integer'):
            h1_ok = True
    except Exception:
        pass

    # H_2: x is an element of R
    h2_ok = False
    try:
        if isinstance(x, MatrixBase):
            if hasattr(R, 'shape'):
                if x.shape == R.shape:
                    h2_ok = True
            elif isinstance(R, str):
                h2_ok = True
            elif isinstance(R, (list, tuple, set)):
                if len(R) > 0 and isinstance(list(R)[0], MatrixBase):
                    if x.shape == list(R)[0].shape:
                        h2_ok = True
            elif R is None:
                h2_ok = True
        elif isinstance(x, int) or hasattr(x, 'is_integer'):
            h2_ok = True
    except Exception:
        pass

    # ¬Q: (x + I is nilpotent) != (x in radical of I)
    neg_q_ok = False
    try:
        if h1_ok and h2_ok and isinstance(x, MatrixBase):
            is_zero_ideal = False
            if isinstance(I, MatrixBase) and I.is_zero:
                is_zero_ideal = True
            elif isinstance(I, (list, tuple, set)) and len(I) > 0 and all(isinstance(m, MatrixBase) and m.is_zero for m in I):
                is_zero_ideal = True
            elif I == 0:
                is_zero_ideal = True
                
            if is_zero_ideal:
                # For the zero ideal in a matrix ring over a field, the radical is {0}.
                in_radical = bool(x.is_zero)
                
                # x + I is nilpotent iff x is nilpotent
                n = x.rows
                is_nilpotent = bool((x**n).is_zero)
                
                neg_q_ok = (is_nilpotent != in_radical)
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: x is an element of R",
    "¬Q: (x + I is nilpotent) is not equivalent to (x in radical of I)"
]

N_HYP = 2
NEG_Q_INDEX = 2