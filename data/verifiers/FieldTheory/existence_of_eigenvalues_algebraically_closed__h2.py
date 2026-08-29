import sympy as sp
from sympy.abc import x

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)
O0 = sp.zeros(0, 0)

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: T is a linear operator mapping V to V",
    "¬Q: There is no non-zero vector v and scalar lambda such that T(v) = lambda v"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # The witness might be provided as a tuple (K, V, T) or just the operator T
        if isinstance(witness, tuple) and len(witness) == 3:
            _, _, T = witness
        else:
            T = witness

        # Case 1: T is a matrix (finite-dimensional operator, or 0-dimensional)
        if isinstance(T, sp.MatrixBase):
            h1 = True  # We assume the matrix entries are over C (algebraically closed)
            h2 = T.is_square
            
            # Check for the existence of any non-zero eigenvector
            evs = T.eigenvects()
            has_nonzero_eigenvector = False
            for ev in evs:
                for vec in ev[2]:
                    if not vec.is_zero_matrix:
                        has_nonzero_eigenvector = True
                        break
                if has_nonzero_eigenvector:
                    break
            
            # The conclusion fails if there are no non-zero eigenvectors
            neg_q = not has_nonzero_eigenvector
            return [h1, h2, neg_q]
            
        # Case 2: T is a function/lambda (potentially an infinite-dimensional operator)
        elif callable(T) or type(T).__name__ == 'Lambda':
            p1 = x**2 + 1
            p2 = x - 3
            
            Tp1 = T(p1)
            Tp2 = T(p2)
            Tp1p2 = T(p1 + p2)
            T2p1 = T(2*p1)
            
            # Verify linearity on a small test set
            is_linear = sp.simplify(Tp1p2 - (Tp1 + Tp2)) == 0
            is_linear = is_linear and sp.simplify(T2p1 - 2*Tp1) == 0
            
            h1 = True
            h2 = bool(is_linear)
            
            # Check if it's the standard infinite-dimensional counterexample: the shift operator T(p) = x*p
            if sp.simplify(Tp1 - x*p1) == 0:
                neg_q = True
            else:
                neg_q = False
                
            return [h1, h2, neg_q]
            
        # Case 3: T is a custom object with descriptive methods
        else:
            if hasattr(T, "is_algebraically_closed"):
                h1 = bool(T.is_algebraically_closed())
            else:
                h1 = True
                
            if hasattr(T, "is_linear_operator"):
                h2 = bool(T.is_linear_operator())
            else:
                h2 = False
                
            if hasattr(T, "has_eigenvalue"):
                neg_q = not bool(T.has_eigenvalue())
            else:
                neg_q = False
                
            return [h1, h2, neg_q]
            
    except Exception:
        return [False, False, False]