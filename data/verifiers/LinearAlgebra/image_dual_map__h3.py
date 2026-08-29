import sympy
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (which we expect to be a tuple or object representing V, W, and T),
    check the remaining hypotheses and the negated conclusion.
    
    For the purpose of this verifier, we assume the witness is a sympy Matrix representing
    a linear transformation T from V to W (where V and W are finite-dimensional vector spaces
    over a field F, represented by the column and row spaces of the matrix).
    
    Wait, if T is a matrix, it is a linear transformation, and the conclusion im(T^*) = (ker(T))^0
    is ALWAYS true for finite-dimensional vector spaces. The conjecture is mathematically FALSE
    only if T is NOT a linear transformation, but the dual map T^* is still defined and maps W^* to V^*.
    However, any map T whose dual maps W^* to V^* must be linear.
    The only way the conclusion fails is if the spaces are infinite-dimensional, but the remaining
    hypotheses explicitly state they are finite-dimensional.
    
    Since we must provide a verifier that evaluates the conditions, we will evaluate them
    based on the matrix representation. If the witness is a matrix, the conclusion will hold,
    so neg_Q will be False. To find a true counterexample, the witness would have to be a
    non-linear map or an infinite-dimensional operator, which we can approximate or check
    properties of. For this verifier, we will check if the witness is a Matrix, and compute
    the spaces to check equality.
    """
    # H1: V and W are vector spaces over a field F
    # H2: V and W are finite-dimensional
    # H3: T^*: W^* \to V^* is the dual map of T
    # ¬Q: im(T^*) != (ker(T))^0
    
    try:
        # We assume the witness is a sympy Matrix representing T
        T = witness
        if not isinstance(T, Matrix):
            return [False, False, False, False]
            
        # H1: V and W are vector spaces over a field F (implicitly true for Matrix over sympy fields)
        h1 = True
        
        # H2: V and W are finite-dimensional (Matrix dimensions are finite)
        h2 = T.rows < float('inf') and T.cols < float('inf')
        
        # H3: T^* is the dual map of T (For matrices, T^* is the transpose)
        T_star = T.transpose()
        h3 = True
        
        # Conclusion: im(T^*) = (ker(T))^0
        # im(T^*) is the column space of T^T
        im_T_star = T_star.columnspace()
        
        # ker(T) is the nullspace of T
        ker_T = T.nullspace()
        
        # (ker(T))^0 is the annihilator of ker(T)
        if not ker_T:
            # If ker(T) is trivial, its annihilator is the whole dual space V^*
            # Represented by the standard basis of V^*
            n = T.cols
            annihilator = eye(n).columnspace()
        else:
            # The annihilator of ker(T) is the nullspace of the matrix formed by ker(T) vectors as rows
            ker_matrix = Matrix.hstack(*ker_T).transpose()
            annihilator = ker_matrix.nullspace()
            
        # Check if the spaces are equal by checking if they span the same space
        # We do this by checking if the rank of the combined basis equals the rank of each
        if not im_T_star and not annihilator:
            spaces_equal = True
        elif not im_T_star or not annihilator:
            spaces_equal = False
        else:
            mat_im = Matrix.hstack(*im_T_star)
            mat_ann = Matrix.hstack(*annihilator)
            mat_combined = Matrix.hstack(mat_im, mat_ann)
            spaces_equal = (mat_im.rank() == mat_ann.rank() == mat_combined.rank())
            
        neg_q = not spaces_equal
        
    except Exception:
        h1 = False
        h2 = False
        h3 = False
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: V and W are finite-dimensional",
    "H_3: T^*: W^* \\to V^* is the dual map of T",
    "¬Q: im(T^*) != (ker(T))^0"
]

N_HYP = 3
NEG_Q_INDEX = 3