import sympy
from sympy import Matrix, MatrixBase, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and FAILS the conclusion.
    The conclusion is: dim(T^{-1}(U)) = dim(U \cap im(T)) + dim(ker(T))
    """
    h1, h2, h3, neg_q = False, False, False, False
    
    # 1. Check if witness is a dictionary explicitly providing the dimensions
    try:
        if isinstance(witness, dict):
            if 'dim_T_inv_U' in witness and 'dim_U_cap_im_T' in witness and 'dim_ker_T' in witness:
                h1 = bool(witness.get('is_vector_space', True))
                h2 = bool(witness.get('is_linear_map', True))
                h3 = bool(witness.get('is_subspace', True))
                
                dim_T_inv_U = witness['dim_T_inv_U']
                dim_U_cap_im_T = witness['dim_U_cap_im_T']
                dim_ker_T = witness['dim_ker_T']
                
                neg_q = not (dim_T_inv_U == dim_U_cap_im_T + dim_ker_T)
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 2. Check if witness is an object explicitly providing the dimensions
    try:
        if hasattr(witness, 'dim_T_inv_U') and hasattr(witness, 'dim_U_cap_im_T') and hasattr(witness, 'dim_ker_T'):
            h1 = bool(getattr(witness, 'is_vector_space', True))
            h2 = bool(getattr(witness, 'is_linear_map', True))
            h3 = bool(getattr(witness, 'is_subspace', True))
            
            dim_T_inv_U = witness.dim_T_inv_U
            dim_U_cap_im_T = witness.dim_U_cap_im_T
            dim_ker_T = witness.dim_ker_T
            
            neg_q = not (dim_T_inv_U == dim_U_cap_im_T + dim_ker_T)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 3. Check if witness is a tuple (T, U) representing the linear map and subspace
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            T, U = witness
            
            # Convert lists/tuples of basis vectors to a matrix whose columns span U
            if isinstance(U, (list, tuple)):
                if len(U) > 0:
                    if isinstance(U[0], (list, tuple)):
                        U = Matrix([list(u) for u in U]).T
                    elif hasattr(U[0], 'tolist'):
                        U = Matrix([list(u) for u in U]).T
                    else:
                        U = Matrix(U)
                else:
                    if hasattr(T, 'rows'):
                        U = Matrix(T.rows, 0, [])
                    
            if isinstance(T, MatrixBase) and isinstance(U, MatrixBase):
                h1 = True
                h2 = True
                h3 = (T.rows == U.rows)
                
                if h3:
                    n = T.cols
                    dim_U = U.rank()
                    dim_im_T = T.rank()
                    dim_ker_T = n - dim_im_T
                    
                    # Dimension of the sum of the images: im(T) + U
                    T_and_U = T.row_join(U)
                    dim_T_and_U = T_and_U.rank()
                    
                    # dim(U \cap im(T)) = dim(im(T)) + dim(U) - dim(im(T) + U)
                    dim_U_cap_im_T = dim_im_T + dim_U - dim_T_and_U
                    
                    # dim(T^{-1}(U)) = n + dim(U) - dim(im(T) + U)
                    dim_T_inv_U = n + dim_U - dim_T_and_U
                    
                    neg_q = not (dim_T_inv_U == dim_U_cap_im_T + dim_ker_T)
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: T: V to W is a linear map",
    "H_3: U is a subspace of W",
    "¬Q: dim(T^{-1}(U)) != dim(U \\cap im(T)) + dim(ker(T))"
]

N_HYP = 3
NEG_Q_INDEX = 3