import sympy as sp

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture:
    "The characteristic polynomial of A^{-1} is given by p_{A^{-1}}(t) = \frac{(-t)^n}{\det(A)} p_A(1/t)"
    """
    # H_1: A is an invertible n \times n matrix over F
    try:
        A = witness
        if not getattr(A, 'is_Matrix', False) or A.rows != A.cols:
            H1 = False
        else:
            det_A = A.det()
            H1 = (det_A != 0)
    except Exception:
        H1 = False

    # H_2: p_A(t) is the characteristic polynomial of A
    try:
        if not getattr(A, 'is_Matrix', False) or A.rows != A.cols:
            H2 = False
        else:
            t = sp.Symbol('t')
            p_A = A.charpoly(t).as_expr()
            H2 = True
    except Exception:
        H2 = False

    # ¬Q: The characteristic polynomial of A^{-1} is NOT given by the formula
    try:
        if not H1 or not H2:
            neg_Q = False
        else:
            n = A.rows
            t = sp.Symbol('t')
            p_A = A.charpoly(t).as_expr()
            A_inv = A.inv()
            p_A_inv = A_inv.charpoly(t).as_expr()
            det_A = A.det()
            
            # Evaluate the right-hand side of the formula
            rhs = ((-t)**n / det_A) * p_A.subs(t, 1/t)
            
            # Check if the actual characteristic polynomial of A^{-1} differs from the formula
            diff = sp.cancel(p_A_inv - rhs)
            neg_Q = (diff != 0)
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: A is an invertible n \\times n matrix over F",
    "H_2: p_A(t) is the characteristic polynomial of A",
    "¬Q: The characteristic polynomial of A^{-1} is NOT given by p_{A^{-1}}(t) = \\frac{(-t)^n}{\\det(A)} p_A(1/t)"
]

N_HYP = 2
NEG_Q_INDEX = 2