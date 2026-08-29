import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, m = witness
            m_provided = True
        else:
            A = witness
            m = None
            m_provided = False
    except Exception:
        A = witness
        m = None
        m_provided = False

    # H1: A is an n x n matrix
    try:
        h1 = bool(hasattr(A, 'is_square') and A.is_square and 
                  hasattr(A, 'shape') and len(A.shape) == 2 and 
                  A.shape[0] == A.shape[1])
    except Exception:
        h1 = False

    # H2: m(t) is the minimal polynomial of A
    try:
        if not h1:
            h2 = False
        else:
            if m_provided:
                m_expr = sympy.sympify(m)
                if hasattr(m_expr, 'as_expr'):
                    m_expr = m_expr.as_expr()
                free_syms = m_expr.free_symbols
                t_sym = list(free_syms)[0] if free_syms else sympy.Symbol('t')
                expected_m = sympy.minpoly(A, t_sym)
                h2 = bool(sympy.expand(m_expr - expected_m) == 0)
            else:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The degree of m(t) is > n
    try:
        if not h1:
            neg_q = False
        else:
            if m_provided:
                m_expr = sympy.sympify(m)
                if hasattr(m_expr, 'as_expr'):
                    m_expr = m_expr.as_expr()
                free_syms = m_expr.free_symbols
                t_sym = list(free_syms)[0] if free_syms else sympy.Symbol('t')
            else:
                t_sym = sympy.Symbol('t')
                m_expr = sympy.minpoly(A, t_sym)
            
            deg_m = sympy.degree(m_expr, gen=t_sym)
            n = A.shape[0]
            neg_q = bool(deg_m > n)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix",
    "H_2: m(t) is the minimal polynomial of A",
    "¬Q: The degree of m(t) is greater than n"
]

N_HYP = 2
NEG_Q_INDEX = 2