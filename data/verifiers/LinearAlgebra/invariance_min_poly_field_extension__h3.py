import sympy
from sympy import Matrix, simplify, eye, zeros
from sympy.abc import x

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

QQ = sympy.polys.domains.QQ
ZZ = sympy.polys.domains.ZZ
RR = sympy.polys.domains.RR
CC = sympy.polys.domains.CC

def to_expr(p):
    """Convert a Poly object or other sympy type to a standard expression."""
    if hasattr(p, 'as_expr'):
        return p.as_expr()
    return sympy.sympify(p)

def conditions(witness):
    """
    Check the hypotheses and the negated conclusion for the false conjecture.
    The dropped hypothesis was the definition of m_F(x), leaving it as a free variable.
    """
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            F = witness.get('F')
            K = witness.get('K')
            m_K = witness.get('m_K')
            m_F = witness.get('m_F')
        else:
            A, F, K, m_K, m_F = witness
    except Exception:
        return [False, False, False, False]

    # H_1: A is an n \times n matrix with entries in a field F
    try:
        h1 = isinstance(A, Matrix) and A.rows == A.cols
        if h1:
            if not getattr(F, 'is_Field', False):
                h1 = False
            else:
                for e in A:
                    try:
                        if e not in F:
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: K is an extension field of F
    try:
        if not getattr(K, 'is_Field', False):
            h2 = False
        else:
            try:
                h2 = (K.unify(F) == K)
            except Exception:
                try:
                    h2 = F.is_subset(K)
                except Exception:
                    h2 = False
    except Exception:
        h2 = False

    # H_3: m_K(x) is the minimal polynomial of A considered over K
    try:
        m_K_expr = to_expr(m_K)
        syms = m_K_expr.free_symbols
        var = list(syms)[0] if syms else x
        expected_m_K = to_expr(A.minpoly(var))
        h3 = sympy.simplify(m_K_expr - expected_m_K) == 0
    except Exception:
        h3 = False

    # ¬Q: m_F(x) != m_K(x)  (The conclusion m_F(x) = m_K(x) fails)
    try:
        m_F_expr = to_expr(m_F)
        m_K_expr = to_expr(m_K)
        neg_q = sympy.simplify(m_F_expr - m_K_expr) != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with entries in a field F",
    "H_2: K is an extension field of F",
    "H_3: m_K(x) is the minimal polynomial of A considered over K",
    "¬Q: m_F(x) != m_K(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3