import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) > 0:
            witness = witness[0]

        if type(witness).__name__ == 'FreeGroup':
            n = len(witness.generators)
            h1 = True
            h2 = True
            neg_q = (n < 2)
        elif type(witness).__name__ == 'FpGroup':
            if len(witness.relators) == 0:
                n = len(witness.generators)
                h1 = True
                h2 = True
                neg_q = (n < 2)
        elif hasattr(witness, 'is_trivial') and witness.is_trivial == True:
            h1 = True
            h2 = True
            neg_q = True
        elif isinstance(witness, int):
            if witness >= 0:
                h1 = True
                h2 = True
                neg_q = (witness < 2)
        elif hasattr(witness, 'is_integer') and witness.is_integer == True:
            n = int(witness)
            if n >= 0:
                h1 = True
                h2 = True
                neg_q = (n < 2)
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group of finite rank n",
    "H_2: F' is the commutator subgroup of F",
    "¬Q: F' is not a free group of countably infinite rank"
]

N_HYP = 2
NEG_Q_INDEX = 2