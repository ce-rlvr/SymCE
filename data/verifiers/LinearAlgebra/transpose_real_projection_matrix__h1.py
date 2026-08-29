import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        def check_Q(P):
            # P must be a square matrix
            if not hasattr(P, 'is_square') or not P.is_square:
                return False
            
            PT = P.T
            
            # Check if P^T is a projection matrix (P^T * P^T == P^T)
            diff = PT * PT - PT
            for e in diff:
                if sympy.simplify(e) != 0:
                    return False
                
            # Check if Range(P^T) is the orthogonal complement of Null(P)
            col_PT = PT.columnspace()
            null_P = P.nullspace()
            
            for v in col_PT:
                for u in null_P:
                    if sympy.simplify(v.dot(u)) != 0:
                        return False
                        
            if len(col_PT) + len(null_P) != P.shape[0]:
                return False
                
            # Check if Null(P^T) is the orthogonal complement of Range(P)
            col_P = P.columnspace()
            null_PT = PT.nullspace()
            
            for v in col_P:
                for u in null_PT:
                    if sympy.simplify(v.dot(u)) != 0:
                        return False
                        
            if len(col_P) + len(null_PT) != P.shape[0]:
                return False
                
            return True

        q_ok = check_Q(witness)
        neg_q = not q_ok
    except Exception:
        # If evaluation fails, the witness does not satisfy the conclusion
        neg_q = True

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: P^T is not a projection matrix with the required orthogonal complement properties"
]

N_HYP = 0
NEG_Q_INDEX = 0