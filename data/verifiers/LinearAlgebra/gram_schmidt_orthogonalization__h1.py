import sympy
from sympy import Matrix, simplify

# Standard linear algebra objects
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a list or tuple of vectors (e.g., sympy.Matrix objects).
    """
    if not isinstance(witness, (list, tuple)):
        return [False, False]
        
    # H_1: {v_1, ..., v_n} is a linearly independent subset of V.
    try:
        if not witness:
            h1 = True
        else:
            cols = []
            for v in witness:
                if not isinstance(v, Matrix):
                    v = Matrix(v)
                cols.append(v.reshape(len(v), 1))
            M = Matrix.hstack(*cols)
            h1 = (M.rank() == len(witness))
    except Exception:
        h1 = False
        
    # neg_Q: Conclusion fails
    # The conclusion states there exists an orthonormal set {e_1, ..., e_n} 
    # such that span(e_1, ..., e_k) = span(v_1, ..., v_k) for all k.
    # This fails if the Gram-Schmidt process encounters an isotropic vector 
    # (a non-zero vector with zero dot product with itself), making normalization impossible.
    try:
        if not witness:
            neg_q = False
        else:
            conclusion_holds = True
            u_list = []
            for v in witness:
                if not isinstance(v, Matrix):
                    v = Matrix(v)
                v = v.reshape(len(v), 1)
                u = v
                for u_prev in u_list:
                    norm_sq = simplify(u_prev.dot(u_prev))
                    if norm_sq == 0:
                        conclusion_holds = False
                        break
                    u = u - u_prev * (simplify(v.dot(u_prev)) / norm_sq)
                
                if not conclusion_holds:
                    break
                
                norm_sq_u = simplify(u.dot(u))
                if norm_sq_u == 0:
                    conclusion_holds = False
                    break
                
                u_list.append(u)
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: {v_1, ..., v_n} is a linearly independent subset of V",
    "¬Q: There does not exist an orthonormal set {e_1, ..., e_n} with the same spans"
]

N_HYP = 1
NEG_Q_INDEX = 1