import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) == 0:
            return [False]
            
        shape = witness[0].shape
        if not all(hasattr(P, 'shape') and P.shape == shape for P in witness):
            return [False]
            
        matrices = [Matrix(P) for P in witness]
        
        sum_P = matrices[0]
        for P in matrices[1:]:
            sum_P = sum_P + P
            
        stacked_P = Matrix.vstack(*matrices)
        
        ns_sum = sum_P.nullspace()
        ns_stacked = stacked_P.nullspace()
        
        def get_rref(ns):
            if not ns:
                return []
            M = Matrix.vstack(*[v.T for v in ns])
            rref_M, _ = M.rref()
            non_zero = []
            for i in range(rref_M.rows):
                row = rref_M.row(i)
                if not all(val == 0 or getattr(val, 'is_zero', False) for val in row):
                    non_zero.append(list(row))
            return non_zero
            
        rref_sum = get_rref(ns_sum)
        rref_stacked = get_rref(ns_stacked)
        
        neg_q = (rref_sum != rref_stacked)
        
        return [bool(neg_q)]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The null space of the sum is not equal to the intersection of the null spaces"
]

N_HYP = 0
NEG_Q_INDEX = 0