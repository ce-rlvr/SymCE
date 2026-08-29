import sympy
from sympy import Matrix, eye, zeros, diag, Rational, lcm, expand, Poly
from sympy.abc import x
from sympy.matrices import MatrixBase

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def matrix_minpoly(M, x):
    """
    Computes the minimal polynomial of a square matrix M.
    """
    if M.rows == 0:
        return Poly(1, x).as_expr()
    
    cp = M.charpoly(x)
    factors = cp.factor_list()
    min_poly = 1
    
    for fac, mult in factors[1]:
        coeffs = fac.all_coeffs()
        degree = len(coeffs) - 1
        fac_M = zeros(M.rows, M.cols)
        M_pow = eye(M.rows)
        
        # Evaluate the irreducible factor at the matrix M
        for i in range(degree, -1, -1):
            fac_M += coeffs[i] * M_pow
            if i > 0:
                M_pow = M_pow * M
        
        # Find the index of nilpotency for this factor's block
        p = 1
        curr_mat = fac_M
        prev_rank = curr_mat.rank()
        while p < mult:
            curr_mat = curr_mat * fac_M
            curr_rank = curr_mat.rank()
            if curr_rank == prev_rank:
                break
            prev_rank = curr_rank
            p += 1
            
        min_poly = min_poly * (fac.as_expr() ** p)
    
    # Ensure the minimal polynomial is monic
    p_obj = Poly(min_poly, x)
    return expand(min_poly / p_obj.LC())

def conditions(witness):
    try:
        if len(witness) == 3:
            A, B, M = witness
        elif len(witness) == 2:
            A, B = witness
            M = diag(A, B)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: Let A and B be square matrices over a field F
    try:
        h1 = (isinstance(A, MatrixBase) and isinstance(B, MatrixBase) and 
              A.rows == A.cols and B.rows == B.cols)
    except Exception:
        h1 = False
        
    # H_2: Let M be the block diagonal matrix with diagonal blocks A and B
    try:
        h2 = isinstance(M, MatrixBase) and M == diag(A, B)
    except Exception:
        h2 = False
        
    # ¬Q: The minimal polynomial of M is NOT the least common multiple of m_A(x) and m_B(x)
    try:
        mA = matrix_minpoly(A, x)
        mB = matrix_minpoly(B, x)
        mM = matrix_minpoly(M, x)
        
        lcm_AB = lcm(mA, mB)
        
        # Ensure the LCM is monic for direct comparison
        p_lcm = Poly(lcm_AB, x)
        lcm_AB = expand(lcm_AB / p_lcm.LC())
        
        diff = expand(mM - lcm_AB)
        neg_q = not (diff == 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are square matrices over a field F",
    "H_2: M is the block diagonal matrix with diagonal blocks A and B",
    "¬Q: The minimal polynomial of M is NOT the least common multiple of m_A(x) and m_B(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2