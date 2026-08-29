import sympy as sp

# Top-level setup for Linear Algebra
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture drops the hypothesis that the vectors v_1, ..., v_n are distinct
    (or equivalently, that n = dim(V)). If the sequence of vectors contains duplicates,
    the set B can still be a valid basis for its span V, but it is impossible to find
    n functionals f_i such that f_i(v_j) = \delta_{ij}, making the conclusion fail.
    """
    try:
        # Extract the sequence of vectors B
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[1], (list, tuple)):
            B = witness[1]
        else:
            B = witness
            
        # Convert to sympy Matrices
        if isinstance(B, sp.Matrix):
            vecs = [B[:, i] for i in range(B.shape[1])]
        else:
            vecs = [sp.Matrix(v) for v in B]
            
        if not vecs:
            # Vacuously true for the trivial vector space {0}
            return [True, True, False]
            
        # Ensure consistent dimensions
        m = vecs[0].shape[0]
        if any(v.shape[0] != m for v in vecs):
            return [False, False, False]
            
        # Standardize to column vectors
        vecs = [v.reshape(v.shape[0] * v.shape[1], 1) for v in vecs]
        
        # H_1: V is finite-dimensional
        # V is implicitly the span of the set B, which is a subspace of R^k, hence finite-dimensional.
        h1 = True
        
        # H_2: B = {v_1, ..., v_n} is a basis for V
        # The SET of vectors B must be linearly independent to be a basis for its span.
        unique_vecs = []
        for v in vecs:
            if v not in unique_vecs:
                unique_vecs.append(v)
                
        if not unique_vecs:
            h2 = True
        else:
            mat_unique = sp.Matrix.hstack(*unique_vecs)
            h2 = bool(mat_unique.rank() == len(unique_vecs))
            
        # Conclusion: There exists a unique basis B^* = {f_1, ..., f_n} for V^* such that f_i(v_j) = \delta_{ij}
        # This holds if and only if the sequence of vectors `vecs` is linearly independent.
        # If there are duplicates (or linear dependencies), no such f_i can exist.
        mat_all = sp.Matrix.hstack(*vecs)
        q = bool(mat_all.rank() == len(vecs))
        
        neg_q = not q
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is finite-dimensional",
    "H_2: B = {v_1, ..., v_n} is a basis for V",
    "¬Q: There does not exist a unique dual basis B^* = {f_1, ..., f_n} for V^* such that f_i(v_j) = \\delta_{ij}"
]

N_HYP = 2
NEG_Q_INDEX = 2