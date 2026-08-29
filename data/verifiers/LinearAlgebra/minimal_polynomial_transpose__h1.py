import sympy as sp

# Top-level setup for Linear Algebra
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    x = sp.Symbol('x')
    
    # H_1: Let A^T denote the transpose of A
    try:
        A_T = witness.T
        h1 = True
    except Exception:
        h1 = False

    # H_2: Let m_A(x) be the minimal polynomial of A
    try:
        m_A = witness.minpoly(x)
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: The minimal polynomial of A^T is NOT exactly equal to m_A(x)
    try:
        m_AT = A_T.minpoly(x)
        
        # Convert to expressions if they are Poly objects
        m_A_expr = m_A.as_expr() if hasattr(m_A, 'as_expr') else m_A
        m_AT_expr = m_AT.as_expr() if hasattr(m_AT, 'as_expr') else m_AT
        
        # Check for mathematical equality
        diff = sp.simplify(m_A_expr - m_AT_expr)
        
        if hasattr(diff, 'equals'):
            eq_zero = diff.equals(0)
            if eq_zero is None:
                # If SymPy cannot prove they are equal, we assume they are not exactly equal
                neg_q = True
            else:
                neg_q = not eq_zero
        else:
            neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A has a transpose A^T",
    "H_2: A has a minimal polynomial m_A(x)",
    "¬Q: The minimal polynomial of A^T is NOT exactly equal to m_A(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2