import sympy
from sympy import Symbol, Matrix, simplify, eye, zeros
from sympy.abc import x

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "H_2: m(x) is the minimal polynomial of A",
    "H_3: c is a scalar",
    "¬Q: c is a root of p(x) is not equivalent to c is a root of m(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            m = witness.get('m')
            c = witness.get('c')
            p = witness.get('p')
        else:
            A, m, c, p = witness
    except Exception:
        return [False, False, False, False]

    # H1: A is an n x n matrix over a field F
    try:
        h1 = isinstance(A, Matrix) and A.is_square
    except Exception:
        h1 = False

    # H2: m(x) is the minimal polynomial of A
    try:
        x_sym = Symbol('x')
        min_poly = A.minimal_polynomial(x_sym)
        
        m_obj = m
        if hasattr(m_obj, 'as_expr'):
            m_obj = m_obj.as_expr()
            
        if callable(m_obj):
            m_expr = m_obj(x_sym)
        else:
            vars_m = m_obj.free_symbols
            if vars_m:
                v = list(vars_m)[0]
                m_expr = m_obj.subs(v, x_sym)
            else:
                m_expr = m_obj
                
        diff = m_expr - min_poly
        h2 = bool(diff.expand() == 0) or bool(simplify(diff) == 0)
    except Exception:
        h2 = False

    # H3: c is an element of F
    try:
        h3 = not getattr(c, 'is_Matrix', False) and not isinstance(c, (list, tuple, dict))
        # Check if c can participate in basic arithmetic (acts like a scalar)
        _ = c + 1
    except Exception:
        h3 = False

    # neg_Q: c is a root of p(x) iff c is a root of m(x) (must fail)
    try:
        p_obj = p
        if hasattr(p_obj, 'as_expr'):
            p_obj = p_obj.as_expr()
            
        if callable(p_obj):
            p_val = p_obj(c)
        else:
            vars_p = p_obj.free_symbols
            if vars_p:
                v_p = list(vars_p)[0]
                p_val = p_obj.subs(v_p, c)
            else:
                p_val = p_obj
        
        m_obj = m
        if hasattr(m_obj, 'as_expr'):
            m_obj = m_obj.as_expr()
            
        if callable(m_obj):
            m_val = m_obj(c)
        else:
            vars_m = m_obj.free_symbols
            if vars_m:
                v_m = list(vars_m)[0]
                m_val = m_obj.subs(v_m, c)
            else:
                m_val = m_obj
        
        root_p = bool(simplify(p_val) == 0)
        root_m = bool(simplify(m_val) == 0)
        
        neg_q = (root_p != root_m)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]