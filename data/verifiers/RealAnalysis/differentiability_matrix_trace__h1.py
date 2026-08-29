import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Check if witness is a square matrix
        if not getattr(witness, 'is_Matrix', False):
            return [False]
        if witness.rows != witness.cols:
            return [False]
            
        n = witness.rows
        
        # Define a symbolic matrix H of the same dimensions
        H = sympy.MatrixSymbol('H', n, n)
        H_mat = sympy.Matrix(H)
        
        # Dummy variable for differentiation to avoid clashes with symbols in witness
        t = sympy.Dummy('t', real=True)
        
        # Evaluate the trace of (A + tH)
        expr = (witness + t * H_mat).trace()
        
        # Compute the directional derivative at t = 0
        deriv = sympy.diff(expr, t).subs(t, 0)
        
        # The expected derivative is the linear map H ↦ tr(H)
        expected = H_mat.trace()
        
        # Check if the computed derivative matches the expected linear map
        diff_expr = sympy.simplify(deriv - expected)
        conclusion_holds = (diff_expr == 0)
        
        # neg_Q is True if the conclusion fails
        neg_q = not conclusion_holds
        
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The trace operator is not differentiable at A, or its derivative is not H ↦ tr(H)"
]

N_HYP = 0
NEG_Q_INDEX = 0