import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

class Ring:
    def __init__(self, is_ring=True):
        self.is_ring = is_ring

class Module:
    def __init__(self, is_noetherian=True):
        self.is_noetherian = is_noetherian

R_ring = Ring(True)
R_not_ring = Ring(False)

M_noeth = Module(True)
M_not_noeth = Module(False)

L_noeth = Module(True)
L_not_noeth = Module(False)

N_noeth = Module(True)
N_not_noeth = Module(False)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('R_is_ring', True))
            m_noeth = bool(witness.get('M_is_Noetherian', False))
            l_noeth = bool(witness.get('L_is_Noetherian', False))
            n_noeth = bool(witness.get('N_is_Noetherian', False))
        else:
            R, L, M, N = witness
            
            if hasattr(R, 'is_ring'):
                h1 = bool(R.is_ring)
            elif R in [ZZ, QQ] or R == 'ring':
                h1 = True
            else:
                h1 = bool(R)
                
            l_noeth = bool(getattr(L, 'is_noetherian', bool(L)))
            m_noeth = bool(getattr(M, 'is_noetherian', bool(M)))
            n_noeth = bool(getattr(N, 'is_noetherian', bool(N)))
            
        neg_q = bool(m_noeth != (l_noeth and n_noeth))
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: M is Noetherian if and only if both L and N are Noetherian modules is false"
]

N_HYP = 1
NEG_Q_INDEX = 1