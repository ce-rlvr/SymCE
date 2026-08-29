import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_scalar(mat):
    """Helper to extract a scalar from a 1x1 matrix or return the scalar itself."""
    try:
        return mat[0]
    except (TypeError, IndexError):
        return mat

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the Min-Max Theorem for Rayleigh Quotients.
    Returns a list of booleans: [H_1, H_2, H_3, neg_Q].
    """
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    # Parse witness and check H1: T is a self-adjoint linear operator on V
    try:
        if hasattr(witness, 'T') and hasattr(witness, 'x'):
            T = witness.T
            x = witness.x
            if hasattr(witness, 'inner_product'):
                ip = witness.inner_product
            else:
                ip = lambda u, v: get_scalar(u.H * v)
            
            if hasattr(witness, 'is_self_adjoint'):
                h1 = bool(witness.is_self_adjoint())
            else:
                h1 = bool(T == T.H)
                
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                # Witness provides a custom metric tensor G for the inner product
                T, x, G = witness
                ip = lambda u, v: get_scalar(u.H * G * v)
                h1 = bool(G * T == T.H * G)
            elif len(witness) == 2:
                # Standard inner product
                T, x = witness
                ip = lambda u, v: get_scalar(u.H * v)
                h1 = bool(T == T.H)
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        h1 = False

    # Check H2: \lambda_{\min} and \lambda_{\max} are the minimum and maximum eigenvalues of T
    try:
        if hasattr(T, 'eigenvals'):
            evals_res = T.eigenvals()
            if isinstance(evals_res, dict):
                evals = list(evals_res.keys())
            else:
                evals = list(evals_res)
        elif hasattr(T, 'eigenvalues'):
            evals_res = T.eigenvalues()
            if isinstance(evals_res, dict):
                evals = list(evals_res.keys())
            else:
                evals = list(evals_res)
        else:
            evals = []
            
        if evals:
            lam_min = min(evals)
            lam_max = max(evals)
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # Check H3: x is a non-zero vector in V
    try:
        if hasattr(x, 'is_zero') and x.is_zero is not None:
            h3 = not bool(x.is_zero)
        else:
            h3 = any(e != 0 for e in x)
    except Exception:
        h3 = False

    # Check negated conclusion: Rayleigh quotient is NOT bounded by the minimum and maximum eigenvalues
    try:
        Tx = T * x
        num = ip(Tx, x)
        den = ip(x, x)
        
        if den == 0:
            # Division by zero means the standard inequality fails to hold
            neg_q = True
        else:
            rayleigh = num / den
            
            # Evaluate inequalities
            lower_check = sp.sympify(lam_min <= rayleigh)
            upper_check = sp.sympify(rayleigh <= lam_max)
            
            # If either inequality evaluates strictly to False, the conclusion fails
            if lower_check == False or upper_check == False:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: T is a self-adjoint linear operator on V",
    "H_2: \\lambda_{\\min} and \\lambda_{\\max} are the minimum and maximum eigenvalues of T respectively",
    "H_3: x is a non-zero vector in V",
    "¬Q: Rayleigh quotient is not bounded by the minimum and maximum eigenvalues"
]

N_HYP = 3
NEG_Q_INDEX = 3