import sympy
from sympy import Matrix, eye, zeros, Poly, lcm
from sympy.abc import x

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_restriction(T, W):
    """
    Computes the matrix of the restriction of operator T to the subspace spanned by W.
    """
    basis = W.columnspace()
    if not basis:
        return zeros(0, 0)
    
    B = basis[0]
    for b in basis[1:]:
        B = B.row_join(b)
    
    n = T.rows
    k = B.cols
    
    # Extend B to a full basis of V
    I = eye(n)
    P = B
    for i in range(n):
        if P.cols == n:
            break
        col = I[:, i]
        if P.row_join(col).rank() > P.cols:
            P = P.row_join(col)
            
    P_inv = P.inv()
    T_sim = P_inv * T * P
    
    # The top-left k x k block is the matrix of T restricted to W
    A = T_sim[:k, :k]
    return A

def make_monic(p):
    """
    Returns the monic version of polynomial p.
    """
    if p == 0:
        return p
    poly = Poly(p, x)
    lc = poly.LC()
    return sympy.expand(p / lc)

def conditions(witness):
    """
    Given a witness tuple (T, W1, W2), checks the hypotheses and negated conclusion.
    T is the matrix of the operator.
    W1, W2 are matrices whose columns span the respective subspaces.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        T = Matrix(witness[0])
        W1 = Matrix(witness[1])
        W2 = Matrix(witness[2])
    except Exception:
        return [False, False, False]
        
    # H_1: Let V be a finite-dimensional vector space.
    try:
        h1 = (T.rows == T.cols) and (W1.rows == T.rows) and (W2.rows == T.rows)
    except Exception:
        h1 = False
        
    # H_2: Let V = W_1 \oplus W_2 where W_1 and W_2 are T-invariant subspaces of V.
    try:
        n = T.rows
        rank_W1 = W1.rank()
        rank_W2 = W2.rank()
        W = W1.row_join(W2)
        
        # Check V = W_1 \oplus W_2
        is_direct_sum = (W.rank() == n) and (rank_W1 + rank_W2 == n)
        
        # Check T-invariance
        inv1 = (W1.row_join(T * W1).rank() == rank_W1)
        inv2 = (W2.row_join(T * W2).rank() == rank_W2)
        
        h2 = is_direct_sum and inv1 and inv2
    except Exception:
        h2 = False
        
    # ¬Q: The minimal polynomial of T is NOT the least common multiple of the 
    # minimal polynomials of the restriction operators T|_{W_1} and T|_{W_2}.
    try:
        A1 = get_restriction(T, W1)
        A2 = get_restriction(T, W2)
        
        m1 = sympy.S.One if A1.rows == 0 else A1.minpoly(x)
        m2 = sympy.S.One if A2.rows == 0 else A2.minpoly(x)
        
        m_lcm = lcm(m1, m2)
        m_T = sympy.S.One if T.rows == 0 else T.minpoly(x)
        
        m_lcm_monic = make_monic(m_lcm)
        m_T_monic = make_monic(m_T)
        
        diff = sympy.expand(m_lcm_monic - m_T_monic)
        neg_q = (diff != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: V = W_1 \\oplus W_2 where W_1 and W_2 are T-invariant subspaces of V",
    "¬Q: The minimal polynomial of T is NOT the least common multiple of the minimal polynomials of T|_{W_1} and T|_{W_2}"
]

N_HYP = 2
NEG_Q_INDEX = 2