import sympy
from sympy.matrices import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            S = witness.get('S')
        else:
            T, S = witness
    except Exception:
        return [False, False, False]
    
    try:
        if not (hasattr(T, 'is_Matrix') and T.is_Matrix):
            T = sympy.Matrix(T)
        h1 = hasattr(T, 'is_Matrix') and T.is_Matrix
    except Exception:
        h1 = False

    try:
        if not (hasattr(S, 'is_Matrix') and S.is_Matrix):
            S = sympy.Matrix(S)
        h2 = hasattr(S, 'is_Matrix') and S.is_Matrix and S.cols == T.rows
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            # The dual transformation is represented by the transpose matrix.
            # We check if (S * T)^T != T^T * S^T
            ST_T = (S * T).transpose()
            T_T_S_T = T.transpose() * S.transpose()
            diff = ST_T - T_T_S_T
            
            neg_q = False
            for e in diff:
                if sympy.expand(e) != 0:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear transformation",
    "H_2: S is a linear transformation",
    "¬Q: (S ∘ T)* != T* ∘ S*"
]

N_HYP = 2
NEG_Q_INDEX = 2