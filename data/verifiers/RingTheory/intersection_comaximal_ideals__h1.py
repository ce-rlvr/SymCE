import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def rank(basis):
    if not basis:
        return 0
    vecs = [list(M) for M in basis]
    return Matrix(vecs).rank()

def is_in_span(M, basis):
    return rank(basis + [M]) == rank(basis)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If I and J are comaximal ideals of a ring R, then I \cap J = IJ."
    (The dropped hypothesis is that R is a commutative ring).
    
    The witness is expected to be a tuple (R_basis, I_basis, J_basis) where
    each is a list of SymPy matrices representing a basis for the ring/ideal
    as a vector space over a field.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False]
            
        R_basis, I_basis, J_basis = witness
        
        if not isinstance(R_basis, list) or not isinstance(I_basis, list) or not isinstance(J_basis, list):
            return [False, False, False]
            
        for basis in [R_basis, I_basis, J_basis]:
            for M in basis:
                if not isinstance(M, sympy.MatrixBase):
                    return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: I and J are ideals of R
    try:
        h1 = True
        # Check R is closed under multiplication
        for r1 in R_basis:
            for r2 in R_basis:
                if not is_in_span(r1 * r2, R_basis):
                    h1 = False
                    break
            if not h1: break
            
        if h1:
            # Check I is a subset of R
            for i in I_basis:
                if not is_in_span(i, R_basis):
                    h1 = False
                    break
                    
        if h1:
            # Check J is a subset of R
            for j in J_basis:
                if not is_in_span(j, R_basis):
                    h1 = False
                    break
                    
        if h1:
            # Check I is a two-sided ideal
            for i in I_basis:
                for r in R_basis:
                    if not is_in_span(i * r, I_basis) or not is_in_span(r * i, I_basis):
                        h1 = False
                        break
                if not h1: break
                
        if h1:
            # Check J is a two-sided ideal
            for j in J_basis:
                for r in R_basis:
                    if not is_in_span(j * r, J_basis) or not is_in_span(r * j, J_basis):
                        h1 = False
                        break
                if not h1: break
    except Exception:
        h1 = False

    # H2: I and J are comaximal (I + J = R)
    try:
        # Since I and J are subspaces of R, I + J = R iff dim(I + J) == dim(R)
        h2 = rank(I_basis + J_basis) == rank(R_basis)
    except Exception:
        h2 = False

    # ¬Q: I \cap J != IJ
    try:
        dim_I = rank(I_basis)
        dim_J = rank(J_basis)
        dim_I_plus_J = rank(I_basis + J_basis)
        
        # Dimension of intersection: dim(I \cap J) = dim(I) + dim(J) - dim(I + J)
        dim_I_cap_J = dim_I + dim_J - dim_I_plus_J
        
        # Basis for the product ideal IJ
        IJ_basis = [i * j for i in I_basis for j in J_basis]
        dim_IJ = rank(IJ_basis)
        
        # Since IJ is always a subspace of I \cap J for two-sided ideals,
        # they are equal if and only if their dimensions are equal.
        neg_q = (dim_I_cap_J != dim_IJ)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I and J are comaximal (I + J = R)",
    "¬Q: I \\cap J is not equal to IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2