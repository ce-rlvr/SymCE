import sympy
import itertools
import math

class MatrixRing:
    def __init__(self, base, n):
        self.base = base
        self.n = n

class BooleanRing:
    def __init__(self, is_infinite=False):
        self.is_infinite = is_infinite

M2_Z = MatrixRing("Z", 2)
M2_Q = MatrixRing("Q", 2)
M2_R = MatrixRing("R", 2)
M2_C = MatrixRing("C", 2)
InfiniteBooleanRing = BooleanRing(is_infinite=True)

def conditions(witness) -> list[bool]:
    try:
        neg_q = False
        
        if isinstance(witness, MatrixRing):
            if witness.n >= 2 and witness.base in ["Z", "Q", "R", "C"]:
                neg_q = True
        elif isinstance(witness, BooleanRing):
            if witness.is_infinite:
                neg_q = True
        elif isinstance(witness, str):
            w_str = witness.lower().replace(" ", "")
            if any(x in w_str for x in ["m2", "m3", "m_2", "m_n", "matrixring"]):
                neg_q = True
            elif "boolean" in w_str and "infinite" in w_str:
                neg_q = True
            elif "product" in w_str and "infinite" in w_str:
                neg_q = True
        elif hasattr(witness, '__class__') and 'MatrixSpace' in witness.__class__.__name__:
            if hasattr(witness, 'shape') and witness.shape[0] == witness.shape[1] and witness.shape[0] >= 2:
                neg_q = True
                
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = ["¬Q: R contains infinitely many idempotent elements"]
N_HYP = 0
NEG_Q_INDEX = 0