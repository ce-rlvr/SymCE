import sympy
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Given a witness (T, v) where T is a linear transformation (matrix) and v is a vector,
    checks if it is a valid counterexample to the conjecture.
    """
    try:
        T, v = witness
        
        # H1: V is a vector space over a field F
        # We verify this by checking if T and v are valid matrices of compatible dimensions
        h1 = isinstance(T, Matrix) and isinstance(v, Matrix) and T.shape[0] == T.shape[1] and T.shape[1] == v.shape[0] and v.shape[1] == 1
        
        # H2: GL(V) is the general linear group of V
        # T must be an element of GL(V), meaning it is invertible
        h2 = T.det() != 0
        
        # H3: GL(V) acts on P(V) via T.span(u) = span(T(u))
        # This is a definitional property of the action, always true for our setup
        h3 = True
        
        # H4: L is a 1-dimensional subspace in P(V) spanned by a non-zero vector v in V
        h4 = not v.is_zero_matrix
        
        # Conclusion: The stabilizer of L in GL(V) consists exactly of those linear transformations in GL(V) for which v is an eigenvector.
        # We check if T stabilizes L and if v is an eigenvector of T.
        Tv = T * v
        M = v.row_join(Tv)
        
        # v is an eigenvector iff Tv is a scalar multiple of v (since v != 0, rank of [v, Tv] is 1)
        is_eigenvector = M.rank() == 1
        
        # T stabilizes L iff T(L) == L. Since L = span(v), T(L) = span(Tv).
        # span(Tv) == span(v) iff Tv is a non-zero scalar multiple of v.
        stabilizes_L = is_eigenvector and not Tv.is_zero_matrix
        
        # The negated conclusion is True if the equivalence fails at the witness
        neg_q = stabilizes_L != is_eigenvector
        
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: GL(V) is the general linear group of V",
    "H_3: GL(V) acts on P(V) via T.span(u) = span(T(u))",
    "H_4: L is a 1-dimensional subspace spanned by a non-zero vector v",
    "¬Q: The stabilizer of L in GL(V) does not consist exactly of those linear transformations in GL(V) for which v is an eigenvector"
]

N_HYP = 4
NEG_Q_INDEX = 4