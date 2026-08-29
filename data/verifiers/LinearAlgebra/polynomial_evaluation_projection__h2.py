import sympy
from sympy import Matrix, eye, zeros, simplify, MatrixBase
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (P, f), where P is a projection matrix
    and f is a matrix polynomial (provided as a callable or a sympy expression).
    """
    try:
        P, f = witness
    except Exception:
        return [False, False]
        
    # H_1: P is a projection matrix
    try:
        if not isinstance(P, MatrixBase):
            P = Matrix(P)
        if not P.is_square:
            h1 = False
        else:
            diff = simplify(P**2 - P)
            h1 = bool(diff.is_zero_matrix)
    except Exception:
        h1 = False
        
    # neg_Q: The matrix polynomial f(P) does NOT evaluate to f(0)I + (f(1) - f(0))P
    try:
        n = P.shape[0]
        I = eye(n)
        O = zeros(n, n)
        
        if callable(f):
            f_P = f(P)
            f_0 = f(O)
            f_1 = f(I)
            
            # Convert to sympy Matrix if the callable returned lists/tuples
            if isinstance(f_P, (list, tuple)): f_P = Matrix(f_P)
            if isinstance(f_0, (list, tuple)): f_0 = Matrix(f_0)
            if isinstance(f_1, (list, tuple)): f_1 = Matrix(f_1)
        else:
            # Assume f is a sympy expression with a single free variable
            free_vars = list(f.free_symbols)
            if len(free_vars) == 1:
                var = free_vars[0]
                f_P = f.subs(var, P).doit()
                f_0 = f.subs(var, O).doit()
                f_1 = f.subs(var, I).doit()
                
                if hasattr(f_P, 'as_explicit'): f_P = f_P.as_explicit()
                if hasattr(f_0, 'as_explicit'): f_0 = f_0.as_explicit()
                if hasattr(f_1, 'as_explicit'): f_1 = f_1.as_explicit()
            else:
                return [h1, False]
                
        # Evaluate f(0)I + (f(1) - f(0))P
        term1 = f_0 * I
        term2 = (f_1 - f_0) * P
        expected = term1 + term2
        
        diff_q = f_P - expected
        if hasattr(diff_q, 'as_explicit'):
            diff_q = diff_q.as_explicit()
        diff_q = simplify(diff_q)
        
        if hasattr(diff_q, 'is_zero_matrix'):
            neg_q = not bool(diff_q.is_zero_matrix)
        else:
            neg_q = bool(diff_q != 0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a projection matrix",
    "¬Q: The matrix polynomial f(P) does not evaluate to f(0)I + (f(1) - f(0))P"
]

N_HYP = 1
NEG_Q_INDEX = 1