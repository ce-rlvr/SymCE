import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False]
        P, Q = witness
        
        if not (hasattr(P, 'is_Matrix') and P.is_Matrix and hasattr(Q, 'is_Matrix') and Q.is_Matrix):
            return [False]
        if P.shape != Q.shape or P.shape[0] != P.shape[1]:
            return [False]
            
        tr_P = complex(P.trace())
        tr_Q = complex(Q.trace())
        tr_PQ = complex((P * Q).trace())
        
        if abs(tr_PQ.imag) > 1e-9:
            q_holds = False
        elif tr_PQ.real < -1e-9:
            q_holds = False
        elif abs(tr_P.imag) > 1e-9 or abs(tr_Q.imag) > 1e-9:
            q_holds = False
        else:
            q_holds = tr_PQ.real <= min(tr_P.real, tr_Q.real) + 1e-9
            
        neg_q = not q_holds
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: Trace(PQ) is not a non-negative real number bounded above by min(Trace(P), Trace(Q))"
]

N_HYP = 0
NEG_Q_INDEX = 0