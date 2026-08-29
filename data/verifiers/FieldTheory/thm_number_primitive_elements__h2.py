import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from sympy.ntheory import factorint, totient

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

def conditions(witness):
    F_obj = None
    q = None
    
    if isinstance(witness, dict):
        F_obj = witness.get('F', witness.get('F_order', witness.get('order', None)))
        q = witness.get('q', None)
    elif isinstance(witness, tuple) and len(witness) == 2:
        F_obj, q = witness
    else:
        F_obj = witness
        q = None
        
    try:
        if hasattr(F_obj, 'order'):
            F_order = F_obj.order() if callable(F_obj.order) else F_obj.order
        elif hasattr(F_obj, 'mod'):
            F_order = F_obj.mod
        else:
            F_order = int(F_obj)
            
        factors = factorint(F_order)
        h1 = (len(factors) == 1) and (F_order > 1)
    except Exception:
        h1 = False

    try:
        actual = totient(F_order - 1) if F_order > 1 else 0
        
        if q is None:
            neg_q = True
        else:
            try:
                q_val = int(q)
                claimed = totient(q_val - 1) if q_val > 1 else -1
            except Exception:
                claimed = None
            neg_q = actual != claimed
            
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field",
    "¬Q: The number of primitive elements of F is not ϕ(q-1)"
]

N_HYP = 1
NEG_Q_INDEX = 1