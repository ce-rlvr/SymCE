import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_linear_operator', False))
            is_ortho = bool(witness.get('is_orthogonal_projection', False))
            is_idem = bool(witness.get('is_idempotent', False))
            is_self_adj = bool(witness.get('is_self_adjoint', False))
            
            rhs = is_idem and is_self_adj
            neg_q = not (is_ortho == rhs)
            return [h1, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_linear_operator'):
            h1 = bool(witness.is_linear_operator)
            is_ortho = bool(witness.is_orthogonal_projection)
            is_idem = bool(witness.is_idempotent)
            is_self_adj = bool(getattr(witness, 'is_self_adjoint', False))
            
            rhs = is_idem and is_self_adj
            neg_q = not (is_ortho == rhs)
            return [h1, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_square') and witness.is_square:
            h1 = True
            is_proj = (witness**2 == witness)
            is_ortho = is_proj
            if is_proj:
                for c in witness.columnspace():
                    for n in witness.nullspace():
                        if (c.H * n)[0, 0] != 0:
                            is_ortho = False
                            break
            rhs = (witness**2 == witness and witness == witness.H)
            neg_q = not (is_ortho == rhs)
            return [h1, neg_q]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: P is a linear operator on V",
    "¬Q: P is an orthogonal projection onto its range if and only if P^2 = P and P = P* (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1