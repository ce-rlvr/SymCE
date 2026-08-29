import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: X is a compact Hausdorff space and R is a ring of functions on X",
    "H_2: A and B are disjoint closed subsets of X",
    "¬Q: The vanishing ideals I_A and I_B are not comaximal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with:
      - 'X': list of points (representing a finite discrete space, hence compact Hausdorff)
      - 'A': list of points in X
      - 'B': list of points in X
      - 'R_basis': list of tuples, where each tuple represents the values of a basis function on X.
                   The span of R_basis over the rationals forms the ring R.
    """
    try:
        X = witness['X']
        A = witness['A']
        B = witness['B']
        R_basis = witness['R_basis']
    except Exception:
        return [False, False, False]
        
    # H_1: X is a compact Hausdorff space and R is a ring of functions on X
    h1 = False
    M = None
    rank_R = 0
    try:
        # A finite set with discrete topology is compact Hausdorff
        if isinstance(X, (list, tuple)) and len(X) > 0 and len(set(X)) == len(X):
            n = len(X)
            if isinstance(R_basis, (list, tuple)) and len(R_basis) > 0:
                if all(isinstance(v, (list, tuple)) and len(v) == n for v in R_basis):
                    M = sp.Matrix(R_basis)
                    rank_R = M.rank()
                    
                    # Check if the constant function 1 is in R
                    ones = sp.ones(1, n)
                    has_1 = (M.col_join(ones).rank() == rank_R)
                    
                    # Check if R is closed under pointwise multiplication
                    closed = True
                    for u in R_basis:
                        for v in R_basis:
                            uv = sp.Matrix(1, n, [u[i] * v[i] for i in range(n)])
                            if M.col_join(uv).rank() > rank_R:
                                closed = False
                                break
                        if not closed:
                            break
                    
                    h1 = has_1 and closed
    except Exception:
        h1 = False
        
    # H_2: A and B are disjoint closed subsets of X
    h2 = False
    try:
        A_set = set(A)
        B_set = set(B)
        X_set = set(X)
        # In a discrete space, all subsets are closed
        h2 = A_set.issubset(X_set) and B_set.issubset(X_set) and A_set.isdisjoint(B_set)
    except Exception:
        h2 = False
        
    # ¬Q: The vanishing ideals I_A and I_B are NOT comaximal in R
    neg_q = False
    try:
        if M is not None:
            A_indices = [X.index(a) for a in A]
            B_indices = [X.index(b) for b in B]
            
            def get_ideal_basis(mat, indices):
                if not indices:
                    # If the subset is empty, the vanishing ideal is the whole ring
                    return [mat[i, :] for i in range(mat.rows)]
                m_sub = mat[:, indices]
                # Find all linear combinations of basis functions that evaluate to 0 on the subset
                null_sub = m_sub.T.nullspace()
                return [(v.T * mat) for v in null_sub]
                
            I_A_basis = get_ideal_basis(M, A_indices)
            I_B_basis = get_ideal_basis(M, B_indices)
            
            if not I_A_basis and not I_B_basis:
                rank_I_A_B = 0
            else:
                # The sum of ideals I_A + I_B is spanned by the union of their bases
                I_A_B_matrix = sp.Matrix.vstack(*(I_A_basis + I_B_basis))
                rank_I_A_B = I_A_B_matrix.rank()
                
            # I_A and I_B are comaximal iff I_A + I_B = R
            # The negation is that they are not comaximal (i.e., rank(I_A + I_B) < rank(R))
            neg_q = rank_I_A_B < rank_R
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]