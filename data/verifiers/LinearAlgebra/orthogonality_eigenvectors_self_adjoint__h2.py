import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        T, lambda1, lambda2, v1, v2 = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: V is an inner product space
    try:
        h1 = (hasattr(T, 'is_square') and T.is_square and 
              hasattr(v1, 'shape') and hasattr(v2, 'shape') and 
              len(v1.shape) == 2 and len(v2.shape) == 2 and
              v1.shape == (T.rows, 1) and v2.shape == (T.rows, 1))
    except Exception:
        h1 = False

    # H_2: lambda_1 and lambda_2 are distinct eigenvalues of T
    try:
        diff = lambda1 - lambda2
        if diff != 0:
            diff = sympy.simplify(diff)
        h2 = bool(diff != 0)
    except Exception:
        h2 = False

    # H_3: v_1 and v_2 are eigenvectors of T corresponding to lambda_1 and lambda_2 respectively
    try:
        n = T.rows
        zero_vec = zeros(n, 1)
        is_v1_nonzero = bool(v1 != zero_vec)
        is_v2_nonzero = bool(v2 != zero_vec)
        
        diff1 = T * v1 - lambda1 * v1
        diff2 = T * v2 - lambda2 * v2
        
        if diff1 != zero_vec:
            diff1 = sympy.simplify(diff1)
        if diff2 != zero_vec:
            diff2 = sympy.simplify(diff2)
            
        h3 = is_v1_nonzero and is_v2_nonzero and bool(diff1 == zero_vec) and bool(diff2 == zero_vec)
    except Exception:
        h3 = False

    # ¬Q: The inner product <v_1, v_2> is not 0
    try:
        inner_prod = (v1.adjoint() * v2)[0, 0]
        if inner_prod != 0:
            inner_prod = sympy.simplify(inner_prod)
        neg_q = bool(inner_prod != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is an inner product space",
    "H_2: lambda_1 and lambda_2 are distinct eigenvalues of T",
    "H_3: v_1 and v_2 are eigenvectors of T corresponding to lambda_1 and lambda_2 respectively",
    "¬Q: The inner product <v_1, v_2> is not 0"
]

N_HYP = 3
NEG_Q_INDEX = 3