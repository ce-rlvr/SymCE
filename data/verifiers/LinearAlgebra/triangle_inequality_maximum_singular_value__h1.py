import sympy
from sympy import Matrix, eye, zeros
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_max_sv(M):
    if 0 in M.shape:
        return 0.0
    try:
        svs = M.singular_values()
        return max(float(sympy.re(sv.evalf())) for sv in svs)
    except Exception:
        MHM = M.H * M
        evs = MHM.eigenvals().keys()
        return math.sqrt(max(float(sympy.re(ev.evalf())) for ev in evs))

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
        else:
            A, B = witness
            
        if not isinstance(A, sympy.MatrixBase):
            A = sympy.Matrix(A)
        if not isinstance(B, sympy.MatrixBase):
            B = sympy.Matrix(B)
            
        if A.shape != B.shape:
            return [False]
    except Exception:
        return [False]
        
    try:
        max_A = get_max_sv(A)
        max_B = get_max_sv(B)
        max_AB = get_max_sv(A + B)
        
        # neg_Q: sigma_max(A+B) > sigma_max(A) + sigma_max(B)
        # We use a small tolerance to avoid false positives from floating point inaccuracies.
        neg_Q = bool(max_AB > max_A + max_B + 1e-9)
    except Exception:
        neg_Q = False
        
    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: sigma_max(A+B) > sigma_max(A) + sigma_max(B)"
]

N_HYP = 0
NEG_Q_INDEX = 0