import sympy
from sympy import Matrix, Symbol

# Top-level setup: named object bindings
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (f, k), checks if it satisfies the remaining hypotheses
    and falsifies the conclusion.
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            k = witness.get('k')
        else:
            f, k = witness
    except Exception:
        return [False, False]
        
    # H_1: Let k be a positive integer.
    try:
        h1_ok = isinstance(k, (int, sympy.Integer)) and k > 0
    except Exception:
        h1_ok = False
        
    # ¬Q: The function f is NOT continuously differentiable on M_n(R), 
    # OR its gradient at A with respect to the Frobenius inner product is NOT k(A^{k-1})^T.
    try:
        a11 = Symbol('a11', real=True)
        a12 = Symbol('a12', real=True)
        a21 = Symbol('a21', real=True)
        a22 = Symbol('a22', real=True)
        A = Matrix([[a11, a12], [a21, a22]])
        
        f_A = f(A)
        
        # Compute the gradient of f at A with respect to the Frobenius inner product
        grad_f = Matrix([
            [sympy.diff(f_A, a11), sympy.diff(f_A, a12)],
            [sympy.diff(f_A, a21), sympy.diff(f_A, a22)]
        ])
        
        expected_grad = k * (A**(k-1)).T
            
        diff_matrix = grad_f - expected_grad
        
        is_equal = True
        for i in range(2):
            for j in range(2):
                diff_val = sympy.simplify(diff_matrix[i, j])
                if diff_val != 0:
                    is_equal = False
                    break
            if not is_equal:
                break
                
        neg_q_ok = not is_equal
    except Exception:
        # If taking the derivative or evaluating f fails, we consider the conclusion to fail.
        neg_q_ok = True
        
    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "¬Q: f is not continuously differentiable or its gradient is not k(A^{k-1})^T"
]

N_HYP = 1
NEG_Q_INDEX = 1