import sympy
from sympy import Integer
from sympy.combinatorics import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros
import sympy.ntheory as nt

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1_ok = True
    
    neg_q_ok = False
    try:
        if isinstance(witness, (int, Integer)):
            neg_q_ok = False
        elif hasattr(witness, 'jacobson_radical'):
            j_r = witness.jacobson_radical()
            if hasattr(j_r, 'radical'):
                rad_j_r = j_r.radical()
            elif hasattr(j_r, 'nilradical'):
                rad_j_r = j_r.nilradical()
            else:
                rad_j_r = j_r
            neg_q_ok = bool(rad_j_r != j_r)
    except Exception:
        pass
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: J(R) is the Jacobson radical of R",
    "¬Q: The radical of J(R) is not equal to J(R)"
]

N_HYP = 1
NEG_Q_INDEX = 1