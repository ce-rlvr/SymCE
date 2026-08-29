import sympy
from sympy import Matrix, eye, zeros, simplify

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Let A be an n x n complex matrix (and lambdas be a sequence of length n)
    try:
        A, lambdas = witness
        h1 = (
            hasattr(A, 'rows') and 
            hasattr(A, 'cols') and 
            A.rows == A.cols and 
            isinstance(lambdas, (list, tuple)) and 
            len(lambdas) == A.rows
        )
    except Exception:
        h1 = False

    # ¬Q: The trace of A does not equal the sum of lambdas, OR the determinant does not equal the product.
    try:
        A, lambdas = witness
        tr = A.trace()
        dt = A.det()
        
        if not lambdas:
            sum_l = sympy.S.Zero
            prod_l = sympy.S.One
        else:
            sum_l = sympy.Add(*lambdas)
            prod_l = sympy.Mul(*lambdas)
            
        trace_eq = (simplify(tr - sum_l) == 0)
        det_eq = (simplify(dt - prod_l) == 0)
        
        neg_q = not (trace_eq and det_eq)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix and lambdas is a sequence of length n",
    "¬Q: trace(A) != sum(lambdas) or det(A) != prod(lambdas)"
]

N_HYP = 1
NEG_Q_INDEX = 1