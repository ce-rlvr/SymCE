import sympy
from sympy import eye, zeros

# Top-level setup for standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "H_2: ||.|| is an induced matrix norm",
    "¬Q: ρ(A) > ||A||"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, norm_obj = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: A is an n x n complex matrix
    try:
        h1 = hasattr(A, 'is_square') and A.is_square and A.rows > 0
    except Exception:
        h1 = False
        
    # H_2: ||.|| is an induced matrix norm
    # An induced matrix norm (even a mixed one) must satisfy ||I|| = 1, 
    # positive definiteness, absolute homogeneity, and the triangle inequality.
    try:
        if callable(norm_obj):
            norm_func = norm_obj
        elif isinstance(norm_obj, str) and norm_obj == 'max':
            # The max absolute entry norm is the induced (1, inf) mixed matrix norm.
            norm_func = lambda M: max([abs(complex(val.evalf())) for val in M])
        else:
            # Fallback to SymPy's built-in norms (e.g., 1, 2, 'inf')
            norm_func = lambda M: M.norm(norm_obj)
            
        n = A.rows
        I = sympy.eye(n)
        Z = sympy.zeros(n, n)
        
        h2 = True
        # Induced norms must satisfy ||I|| = 1. This naturally filters out the Frobenius norm.
        if abs(float(norm_func(I)) - 1.0) > 1e-7:
            h2 = False
        elif float(norm_func(Z)) != 0.0:
            h2 = False
        else:
            # Deterministic empirical tests for norm properties
            matrices = [
                sympy.Matrix(n, n, lambda i, j: i + j + 1),
                sympy.Matrix(n, n, lambda i, j: i - j),
                sympy.Matrix(n, n, lambda i, j: 1 if i == j else -1)
            ]
            for M in matrices:
                nM = float(norm_func(M))
                if M != Z and nM <= 0:
                    h2 = False
                    break
                # Absolute homogeneity
                ncM = float(norm_func(-2.5 * M))
                if abs(ncM - 2.5 * nM) > 1e-5 * max(1.0, ncM):
                    h2 = False
                    break
                # Triangle inequality
                for B in matrices:
                    nB = float(norm_func(B))
                    nMpB = float(norm_func(M + B))
                    if nMpB > nM + nB + 1e-5:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    # ¬Q: ρ(A) > ||A||
    try:
        evals = A.eigenvals()
        rho = max([abs(complex(ev.evalf())) for ev in evals]) if evals else 0.0
        norm_val = float(norm_func(A))
        # Strict inequality with a small tolerance for floating point safety
        neg_q = rho > norm_val + 1e-7
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]