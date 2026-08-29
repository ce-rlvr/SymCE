import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            A, provided_lmbda = witness
        else:
            A = witness
            provided_lmbda = None
            
        if not hasattr(A, 'shape') or len(A.shape) != 2 or A.shape[0] != A.shape[1]:
            return [False, False, False]
            
        n = A.shape[0]
    except Exception:
        return [False, False, False]

    # H1: The characteristic polynomial of A is of the form (x - lambda)^n for some lambda in F
    h1 = False
    lmbda = None
    try:
        if n == 0:
            h1 = True
            lmbda = provided_lmbda if provided_lmbda is not None else 0
        else:
            x = sympy.Symbol('x')
            cp = A.charpoly(x).as_expr()
            
            if provided_lmbda is not None:
                lmbda = provided_lmbda
                expected_cp = (x - lmbda)**n
                h1 = bool(sympy.simplify(cp - expected_cp) == 0)
            else:
                evs = A.eigenvals()
                if len(evs) == 1:
                    lmbda_calc, mult = list(evs.items())[0]
                    if mult == n:
                        h1 = True
                        lmbda = lmbda_calc
    except Exception:
        h1 = False

    # H2: A is diagonalizable over F
    h2 = False
    try:
        if n == 0:
            h2 = True
        else:
            h2 = bool(A.is_diagonalizable())
    except Exception:
        h2 = False

    # neg_Q: A is NOT equal to lambda I
    neg_q = False
    try:
        if n == 0:
            neg_q = False
        elif lmbda is not None:
            I = sympy.eye(n)
            diff = A - lmbda * I
            is_zero = True
            for i in range(n):
                for j in range(n):
                    if sympy.simplify(diff[i, j]) != 0:
                        is_zero = False
                        break
                if not is_zero:
                    break
            neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The characteristic polynomial of A is of the form (x - lambda)^n for some lambda in F",
    "H_2: A is diagonalizable over F",
    "¬Q: A is not equal to lambda I"
]

N_HYP = 2
NEG_Q_INDEX = 2