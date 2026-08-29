import sympy
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'shape'):
            M = witness
            k = M.shape[0]
            lam = M[0,0] if k > 0 else 0
        elif isinstance(witness, tuple):
            k, lam = witness
            k = int(k)
            M = zeros(k, k)
            for i in range(k):
                M[i, i] = lam
                if i < k - 1:
                    M[i, i+1] = 1
        else:
            k = int(witness)
            lam = 0
            M = zeros(k, k)
            for i in range(k):
                M[i, i] = lam
                if i < k - 1:
                    M[i, i+1] = 1
                    
        if k == 0:
            concl = False
        else:
            I = eye(k)
            A = M - lam * I
            geom_mult = k - A.rank()
            if geom_mult != 1:
                concl = False
            else:
                e1 = I[:, 0]
                if A * e1 != zeros(k, 1):
                    concl = False
                else:
                    concl = True
        neg_q = not concl
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The geometric multiplicity of lambda is not 1, or its eigenspace is not spanned by e_1"
]

N_HYP = 0
NEG_Q_INDEX = 0