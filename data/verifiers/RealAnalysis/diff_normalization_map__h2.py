import sympy
from sympy import Matrix, sympify

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, (int, float)):
            a = Matrix([witness])
        else:
            a = Matrix(witness)
        
        if a.shape[0] < 1:
            h1 = False
        elif a.shape[1] != 1 and a.shape[0] != 1:
            h1 = False
        else:
            # Check if all elements are real
            h1 = all(sympify(val).is_real is not False for val in a)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            if isinstance(witness, (int, float)):
                a = Matrix([witness])
            else:
                a = Matrix(witness)
            if a.shape[0] == 1:
                a = a.T
            
            is_zero = all(sympify(val).is_zero for val in a)
            neg_q = bool(is_zero)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is defined on R^n \\ {0} as x / ||x||",
    "¬Q: f is not continuously differentiable at a with the given Jacobian"
]

N_HYP = 1
NEG_Q_INDEX = 1