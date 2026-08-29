import sympy
from sympy import Matrix, zeros, eye, Symbol, Integer

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Extract n and A from the witness
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            A = witness.get('A')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                n, A = witness
            elif len(witness) == 3:
                K, n, A = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: K is a field
    # In the context of SymPy, we verify that A is a valid matrix object (which operates over a field/ring).
    try:
        h1_ok = hasattr(A, 'charpoly') and hasattr(A, 'is_square')
    except Exception:
        h1_ok = False

    # H_2: n is a positive integer
    try:
        h2_ok = isinstance(n, (int, Integer)) and n > 0
    except Exception:
        h2_ok = False

    # H_3: A is a nilpotent matrix
    try:
        h3_ok = False
        if h1_ok and A.is_square:
            m = A.shape[0]
            h3_ok = bool(A**m == zeros(m, m))
    except Exception:
        h3_ok = False

    # ¬Q: The characteristic polynomial of A is not x^n
    try:
        x = Symbol('x')
        char_poly = A.charpoly(x).as_expr()
        expected_poly = x**n
        neg_q_ok = bool(sympy.expand(char_poly - expected_poly) != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n is a positive integer",
    "H_3: A is a nilpotent matrix",
    "¬Q: The characteristic polynomial of A is not x^n"
]

N_HYP = 3
NEG_Q_INDEX = 3