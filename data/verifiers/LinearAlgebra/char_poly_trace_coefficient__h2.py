import sympy
from sympy import Matrix, eye, Symbol, Poly

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an n x n matrix over a field F
    try:
        if isinstance(witness, (list, tuple)):
            witness = Matrix(witness)
        if not (hasattr(witness, 'rows') and hasattr(witness, 'cols')):
            return [False, False]
        if witness.rows != witness.cols:
            return [False, False]
        n = witness.rows
        if n < 1:
            return [False, False]
        trace = witness.trace()
        H1 = True
    except Exception:
        return [False, False]
        
    # ¬Q: The coefficient c_{n-1} is not equal to -Tr(A)
    try:
        x_sym = Symbol('__x_char_poly')
        I = eye(n)
        # The characteristic polynomial is defined here as det(A - xI)
        # to match the context where c_{n-1} = -Tr(A) can be false (e.g., for odd n).
        char_poly = (witness - x_sym * I).det()
        p = Poly(char_poly, x_sym)
        c_n_minus_1 = p.nth(n - 1)
        
        diff = sympy.simplify(c_n_minus_1 + trace)
        neg_Q = (diff != 0)
    except Exception:
        neg_Q = False
        
    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field F",
    "¬Q: The coefficient c_{n-1} is not equal to -Tr(A)"
]

N_HYP = 1
NEG_Q_INDEX = 1