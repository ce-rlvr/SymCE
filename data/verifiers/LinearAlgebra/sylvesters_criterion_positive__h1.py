import sympy
from sympy import Matrix, I, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is a symmetric matrix
    try:
        h1 = False
        if hasattr(witness, 'is_square') and witness.is_square:
            h1 = bool(witness == witness.T)
    except Exception:
        h1 = False

    # ¬Q: A is positive definite if and only if all of its leading principal minors are strictly positive is FALSE
    try:
        if not (hasattr(witness, 'is_square') and witness.is_square):
            neg_q = False
        else:
            all_minors_pos = True
            for k in range(1, witness.shape[0] + 1):
                minor = witness[:k, :k].det()
                try:
                    if not bool(minor > 0):
                        all_minors_pos = False
                        break
                except TypeError:
                    # Raised if minor is complex with non-zero imaginary part, or symbolic
                    all_minors_pos = False
                    break

            is_hermitian = bool(witness == witness.conjugate().T)
            is_pd = False
            if is_hermitian:
                if hasattr(witness, 'is_positive_definite'):
                    pd_attr = witness.is_positive_definite
                    if pd_attr is not None:
                        is_pd = bool(pd_attr)
                    else:
                        is_pd = all_minors_pos
                else:
                    is_pd = all_minors_pos
            
            q = (is_pd == all_minors_pos)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a symmetric matrix",
    "¬Q: A is positive definite if and only if all of its leading principal minors are strictly positive is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1