import sympy

x = sympy.Symbol('x')
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            p = witness.get('p')
            m = witness.get('m')
        else:
            A, p, m = witness
    except Exception:
        return [False, False, False]

    # H_1: A is an n x n matrix over a field F
    try:
        h1 = isinstance(A, sympy.MatrixBase) and A.is_square
    except Exception:
        h1 = False

    # H_2: p is the characteristic polynomial of A
    try:
        p_expr = sympy.sympify(p)
        char_poly = A.charpoly(x).as_expr()
        h2 = bool(sympy.simplify(p_expr - char_poly) == 0)
    except Exception:
        h2 = False

    # neg_Q: m does NOT divide p
    try:
        p_expr = sympy.sympify(p)
        m_expr = sympy.sympify(m)
        if sympy.simplify(m_expr) == 0:
            neg_q = bool(sympy.simplify(p_expr) != 0)
        else:
            q = sympy.cancel(p_expr / m_expr)
            num, den = q.as_numer_denom()
            neg_q = (x in den.free_symbols)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field F",
    "H_2: p is the characteristic polynomial of A",
    "neg_Q: m does not divide p"
]

N_HYP = 2
NEG_Q_INDEX = 2