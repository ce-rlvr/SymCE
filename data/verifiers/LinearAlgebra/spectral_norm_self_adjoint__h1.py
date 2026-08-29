import sympy
from sympy import eye, zeros

# Top-level setup for potential witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H_1: T is a self-adjoint linear operator on V
        # For a matrix or operator, this means it equals its Hermitian conjugate
        h1 = bool(witness == witness.H)
    except Exception:
        h1 = False

    try:
        T = witness
        
        # Get eigenvalues
        eigs_dict = T.eigenvals()
        eigs = list(eigs_dict.keys())
        
        if not eigs:
            has_eigenvalues = False
        else:
            has_eigenvalues = True
            abs_eigs = [sympy.Abs(e) for e in eigs]
            try:
                max_eig = max(abs_eigs)
            except TypeError:
                # Fallback for symbolic/algebraic numbers that cannot be directly compared
                max_eig = max(abs_eigs, key=lambda x: float(x.evalf()))
            
        # Get operator norm (maximum singular value)
        if hasattr(T, 'singular_values'):
            svs = T.singular_values()
            if not svs:
                norm_T = 0
            else:
                try:
                    norm_T = max(svs)
                except TypeError:
                    norm_T = max(svs, key=lambda x: float(x.evalf()))
        else:
            # Fallback if singular_values is not implemented
            t_h_t = T.H * T
            eigs_sq = list(t_h_t.eigenvals().keys())
            if not eigs_sq:
                norm_T = 0
            else:
                sqrt_eigs = [sympy.sqrt(sympy.Abs(e)) for e in eigs_sq]
                try:
                    norm_T = max(sqrt_eigs)
                except TypeError:
                    norm_T = max(sqrt_eigs, key=lambda x: float(x.evalf()))
                
        # Evaluate ¬Q: The operator norm of T does NOT equal the maximum absolute value of its eigenvalues
        if not has_eigenvalues:
            # If there are no eigenvalues (e.g., 0x0 matrix or certain infinite-dimensional operators),
            # the maximum absolute eigenvalue is undefined, so it cannot equal the norm.
            neg_q = True
        else:
            diff = sympy.simplify(norm_T - max_eig)
            if diff == 0:
                neg_q = False
            else:
                try:
                    if hasattr(diff, 'free_symbols') and diff.free_symbols:
                        neg_q = True
                    else:
                        # Numerical check to account for floating point inaccuracies or unsimplified expressions
                        neg_q = bool(abs(float(diff.evalf())) > 1e-9)
                except Exception:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: T is a self-adjoint linear operator on V",
    "¬Q: The operator norm of T does not equal the maximum absolute value of its eigenvalues"
]

N_HYP = 1
NEG_Q_INDEX = 1