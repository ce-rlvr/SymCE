import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: B is a non-degenerate bilinear form on V",
    "H_3: T is a linear operator on V",
    "¬Q: Im(T^*) != (\\ker T)^\\perp"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        B_raw, T_raw = witness
        
        try:
            B = B_raw if hasattr(B_raw, 'is_square') else Matrix(B_raw)
            T = T_raw if hasattr(T_raw, 'is_square') else Matrix(T_raw)
        except Exception:
            return [False, False, False, False]
            
        # H1: V is a finite-dimensional vector space over a field F
        try:
            h1 = bool(B.is_square and T.is_square and B.shape == T.shape)
        except Exception:
            h1 = False
            
        # H2: B is a non-degenerate bilinear form on V
        try:
            h2 = bool(h1 and B.det() != 0)
        except Exception:
            h2 = False
            
        # H3: T is a linear operator on V
        try:
            h3 = h1
        except Exception:
            h3 = False
            
        # neg_Q: Im(T^*) != (\ker T)^\perp
        try:
            if not (h1 and h2 and h3):
                neg_q = False
            else:
                # T^* is the right adjoint: B(Tx, y) = B(x, T^*y) => T^* = B^-1 T^T B
                T_star = B.inv() * T.transpose() * B
                im_T_star = T_star.columnspace()
                
                ker_T = T.nullspace()
                
                if not ker_T:
                    # ker T is trivial, so (ker T)^\perp is V
                    # Im(T^*) is also V since T is invertible
                    neg_q = False
                else:
                    K = ker_T[0]
                    for vec in ker_T[1:]:
                        K = K.row_join(vec)
                    
                    # Left orthogonal complement of ker T:
                    # { x | B(x, y) = 0 for all y in ker T }
                    # x^T B K = 0 => K^T B^T x = 0
                    eq_matrix = K.transpose() * B.transpose()
                    left_perp = eq_matrix.nullspace()
                    
                    if len(im_T_star) != len(left_perp):
                        neg_q = True
                    else:
                        if len(im_T_star) == 0:
                            neg_q = False
                        else:
                            mat_A = im_T_star[0]
                            for v in im_T_star[1:]:
                                mat_A = mat_A.row_join(v)
                            mat_B = left_perp[0]
                            for v in left_perp[1:]:
                                mat_B = mat_B.row_join(v)
                            
                            mat_combined = mat_A.row_join(mat_B)
                            # If the combined matrix has rank greater than the dimension,
                            # the spaces are not equal.
                            neg_q = bool(mat_combined.rank() != len(im_T_star))
        except Exception:
            neg_q = False

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]