import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # The witness could be a tuple (F, G) or just the field F (or its size q)
        if isinstance(witness, tuple) and len(witness) == 2:
            F, G = witness
            witness = F
            
        char = None
        
        # Check if witness is an integer representing the size of a finite field
        if isinstance(witness, int):
            factors = factorint(witness)
            # A finite field exists iff its size is a prime power
            if len(factors) == 1 and witness > 1:
                h1 = True
                char = list(factors.keys())[0]
                
        # Check if witness is a sympy Field object
        elif hasattr(witness, 'characteristic'):
            if callable(witness.characteristic):
                char = witness.characteristic()
            else:
                char = witness.characteristic
            h1 = True
            
        elif hasattr(witness, 'char'):
            if callable(witness.char):
                char = witness.char()
            else:
                char = witness.char
            h1 = True
            
        if h1:
            # If F is a valid field, G = SL(2, F) is satisfied by definition of the witness
            h2 = True
            
        if h1 and char is not None:
            # The center of SL(2, F) consists of scalar matrices lambda * I 
            # where lambda^2 = 1. 
            # In any field, lambda^2 = 1 has at most two solutions: 1 and -1.
            # If the characteristic is 2, then 1 = -1, so there is exactly 1 solution.
            # If the characteristic is not 2, there are exactly 2 distinct solutions.
            # The conclusion states the center has exactly two elements.
            # Therefore, the conclusion fails (neg_Q is True) iff characteristic is 2.
            neg_q = (char == 2)
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: G is the special linear group SL(2, F)",
    "¬Q: The center Z(G) does not consist of exactly two elements"
]

N_HYP = 2
NEG_Q_INDEX = 2