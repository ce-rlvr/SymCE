import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not hasattr(witness, 'is_square') or not witness.is_square:
            return [False]
        n = witness.shape[0]
        tr = witness.trace()
        val = complex(tr)
        neg_q = abs(val) > n
        return [bool(neg_q)]
    except Exception:
        return [False]

CONDITION_LABELS = ["¬Q: |tr(Q)| > n"]
N_HYP = 0
NEG_Q_INDEX = 0