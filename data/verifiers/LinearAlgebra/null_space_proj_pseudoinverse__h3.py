import sympy as sp

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A = witness
        # H_1: A is a matrix
        if not getattr(A, 'is_Matrix', False):
            return [False, False, False]
        h1 = True
        
        # H_2: A^+ is the Moore-Penrose pseudoinverse of A
        # This is a definition applied to the witness, so it holds by computation.
        h2 = True
        
        # Conclusion: I - A^+A is the orthogonal projection operator onto the null space of A
        A_pinv = A.pinv()
        n = A.shape[1]
        I = sp.eye(n)
        P = I - A_pinv * A
        
        # Check if P is an orthogonal projection
        # 1. Idempotent: P^2 = P
        diff_idemp = sp.simplify(P * P - P)
        is_idempotent = (diff_idemp.is_zero_matrix == True)
        
        # 2. Hermitian: P^* = P
        diff_herm = sp.simplify(P.H - P)
        is_hermitian = (diff_herm.is_zero_matrix == True)
        
        # Check if Range(P) is the null space of A
        ns = A.nullspace()
        if ns:
            V = sp.Matrix.hstack(*ns)
            # Px = x for all x in nullspace
            diff_range = sp.simplify(P * V - V)
            range_match = (diff_range.is_zero_matrix == True) and (P.rank() == len(ns))
        else:
            # If null space is trivial, P must be the zero matrix
            range_match = (P.is_zero_matrix == True)
            
        Q = is_idempotent and is_hermitian and range_match
        neg_Q = not Q
        
        return [h1, h2, neg_Q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: A is a matrix in C^{m x n}",
    "H_2: A^+ is the Moore-Penrose pseudoinverse of A",
    "¬Q: I - A^+A is not the orthogonal projection operator onto the null space of A"
]

N_HYP = 2
NEG_Q_INDEX = 2