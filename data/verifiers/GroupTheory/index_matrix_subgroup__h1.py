import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            for item in witness:
                if getattr(item, 'is_Matrix', False) or isinstance(item, list):
                    witness = item
                    break

        if isinstance(witness, list):
            try:
                A = Matrix(witness)
            except Exception:
                return [False, False, False, False]
        else:
            A = witness
            
        if not getattr(A, 'is_Matrix', False):
            return [False, False, False, False]
            
        try:
            h1 = (A.rows == A.cols)
        except Exception:
            h1 = False
        
        try:
            h2 = all(isinstance(x, (int, sp.Integer)) for x in A)
        except Exception:
            h2 = False
        
        try:
            det_A = A.det()
            h3 = bool(det_A != 0)
        except Exception:
            h3 = False
            
        try:
            if not (h1 and h2):
                neg_q = False
            else:
                snf = A.smith_normal_form()
                index = 1
                for i in range(A.rows):
                    index *= snf[i, i]
                
                is_finite = all(snf[i, i] != 0 for i in range(A.rows))
                
                if not is_finite:
                    neg_q = True
                else:
                    neg_q = bool(abs(index) != abs(det_A))
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix",
    "H_2: A has integer entries",
    "H_3: det(A) != 0",
    "¬Q: The index of H in G is infinite or not equal to |det(A)|"
]

N_HYP = 3
NEG_Q_INDEX = 3