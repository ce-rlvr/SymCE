import sympy as sp
from sympy import eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Given a witness (A, c, n), checks if it is a valid counterexample to the false conjecture.
    The dropped hypothesis was "A is an n x n matrix", meaning n is unbound and can be 
    chosen to be different from the dimension of A.
    """
    try:
        A, c, n = witness
    except Exception:
        return [False, False, False]

    # H_1: c is a non-zero scalar in F
    try:
        if isinstance(c, (sp.MatrixBase, list, tuple, dict)):
            h1_ok = False
        else:
            h1_ok = bool(c != 0)
    except Exception:
        h1_ok = False

    # H_2: p_A(x) is the characteristic polynomial of A
    # This implies A must be a square matrix for the characteristic polynomial to be defined.
    try:
        h2_ok = isinstance(A, sp.MatrixBase) and A.is_square
    except Exception:
        h2_ok = False

    # ¬Q: The characteristic polynomial of cA is NOT p_{cA}(x) = c^n * p_A(x/c)
    try:
        x = sp.Symbol('x')
        p_A = A.charpoly(x).as_expr()
        p_cA = (c * A).charpoly(x).as_expr()
        
        # Evaluate c^n * p_A(x/c)
        rhs = (c**n) * p_A.subs(x, x / c)
        
        # Check if they are not equal
        diff = sp.simplify(p_cA - rhs)
        neg_q_ok = bool(diff != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: c is a non-zero scalar in F",
    "H_2: p_A(x) is the characteristic polynomial of A",
    "¬Q: p_{cA}(x) != c^n * p_A(x/c)"
]

N_HYP = 2
NEG_Q_INDEX = 2