import sympy
from sympy import eye, zeros
from sympy.abc import x

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is invertible",
    "H_2: p_A(x) is the characteristic polynomial of A",
    "¬Q: The characteristic polynomial of A^{-1} is not ((-1)^n / det(A)) * x^n * p_A(1/x)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    A = None
    p_A = None
    n = None
    
    # Unpack witness
    # The dropped hypothesis is "A is an n x n matrix", which leaves n as a free variable.
    # A valid counterexample witness must provide A and n (and optionally p_A).
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            p_A = witness.get('p_A')
            n = witness.get('n')
            if A is not None:
                A = sympy.Matrix(A)
                if p_A is None:
                    p_A = A.charpoly(x).as_expr()
                if n is None:
                    n = A.shape[0]
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                A, p_A, n = witness
                A = sympy.Matrix(A)
            elif len(witness) == 2:
                if isinstance(witness[1], (int, float, sympy.Number)):
                    A, n = witness
                    A = sympy.Matrix(A)
                    p_A = A.charpoly(x).as_expr()
                else:
                    A, p_A = witness
                    A = sympy.Matrix(A)
                    n = A.shape[0]
            elif len(witness) == 1:
                A = witness[0]
                A = sympy.Matrix(A)
                n = A.shape[0]
                p_A = A.charpoly(x).as_expr()
        else:
            A = witness
            A = sympy.Matrix(A)
            n = A.shape[0]
            p_A = A.charpoly(x).as_expr()
            
        if n is not None:
            n = int(n)
    except Exception:
        pass

    if A is None or p_A is None or n is None:
        return [False, False, False]

    # H_1: A is invertible
    try:
        h1 = A.is_square and A.det() != 0
    except Exception:
        h1 = False

    # H_2: p_A(x) is the characteristic polynomial of A
    try:
        expected_p_A = A.charpoly(x).as_expr()
        p_A_expr = sympy.sympify(p_A)
        if hasattr(p_A_expr, 'as_expr'):
            p_A_expr = p_A_expr.as_expr()
        diff = sympy.simplify(sympy.expand(p_A_expr - expected_p_A))
        h2 = (diff == 0)
    except Exception:
        h2 = False

    # ¬Q: The characteristic polynomial of A^{-1} is NOT ((-1)^n / det(A)) * x^n * p_A(1/x)
    try:
        A_inv = A.inv()
        p_A_inv = A_inv.charpoly(x).as_expr()
        
        det_A = A.det()
        
        # Substitute x with 1/x in p_A(x)
        p_A_1_over_x = p_A_expr.subs(x, 1/x)
        
        # Compute the formula from the conclusion
        formula = ((-1)**n / det_A) * (x**n) * p_A_1_over_x
        
        # Check if the actual characteristic polynomial of A^{-1} differs from the formula
        diff_q = sympy.simplify(sympy.expand(p_A_inv - formula))
        neg_q = (diff_q != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]