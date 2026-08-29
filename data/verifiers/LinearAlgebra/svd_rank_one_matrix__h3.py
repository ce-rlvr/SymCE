import sympy as sp
from sympy import Matrix, I, zeros, eye

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # The witness is expected to be a tuple (u, v, A) or a dictionary with these keys.
    if isinstance(witness, dict):
        u = witness.get('u')
        v = witness.get('v')
        A = witness.get('A')
    else:
        try:
            u, v, A = witness
        except Exception:
            return [False, False, False]
            
    # H_1: u is a non-zero column vector
    try:
        h1 = isinstance(u, Matrix) and u.shape[1] == 1 and any(sp.simplify(x) != 0 for x in u)
    except Exception:
        h1 = False

    # H_2: v is a non-zero column vector
    try:
        h2 = isinstance(v, Matrix) and v.shape[1] == 1 and any(sp.simplify(x) != 0 for x in v)
    except Exception:
        h2 = False

    # ¬Q: A does NOT have exactly one non-zero singular value equal to ||u||_2 ||v||_2
    try:
        if not isinstance(A, Matrix):
            neg_q = True
        else:
            # Compute eigenvalues of A^* A to find the squared singular values
            A_H = A.H
            M = A_H * A
            evs = M.eigenvals()
            
            nz_evs = []
            for ev, mult in evs.items():
                if sp.simplify(ev) != 0:
                    nz_evs.extend([ev] * mult)
            
            if len(nz_evs) != 1:
                neg_q = True
            else:
                # Calculate squared Euclidean norms of u and v
                norm_u_sq = sum(x * sp.conjugate(x) for x in u)
                norm_v_sq = sum(x * sp.conjugate(x) for x in v)
                expected_val_sq = norm_u_sq * norm_v_sq
                
                # Check if the single non-zero squared singular value matches the expected squared product
                diff = sp.simplify(nz_evs[0] - expected_val_sq)
                if diff == 0:
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: u is a non-zero column vector",
    "H_2: v is a non-zero column vector",
    "¬Q: A does not have exactly one non-zero singular value equal to ||u||_2 ||v||_2"
]

N_HYP = 2
NEG_Q_INDEX = 2