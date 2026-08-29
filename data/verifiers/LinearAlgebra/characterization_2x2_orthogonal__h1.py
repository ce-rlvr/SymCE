import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_eq(x, y):
    try:
        if x == y:
            return True
        diff = x - y
        if hasattr(diff, 'equals'):
            eq = diff.equals(0)
            if eq is True:
                return True
        return sympy.simplify(diff) == 0
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, Matrix):
            try:
                witness = Matrix(witness)
            except Exception:
                pass
                
        if not isinstance(witness, Matrix) or witness.shape != (2, 2):
            neg_q = True
        else:
            a, b, c, d = witness[0, 0], witness[0, 1], witness[1, 0], witness[1, 1]
            
            # Form 1: a = d, b = -c, a^2 + b^2 = 1
            form1 = check_eq(a, d) and check_eq(b, -c) and check_eq(a**2 + b**2, 1)
            
            # Form 2: a = -d, b = c, a^2 + b^2 = 1
            form2 = check_eq(a, -d) and check_eq(b, c) and check_eq(a**2 + b**2, 1)
            
            neg_q = not (form1 or form2)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = ["¬Q: Q is not of the specified orthogonal forms"]

N_HYP = 0
NEG_Q_INDEX = 0