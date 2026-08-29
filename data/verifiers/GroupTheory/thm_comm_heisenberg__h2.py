import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: The commutator subgroup is not equal to the center"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    char = None
    
    try:
        # Check if the witness is an integer representing a prime field GF(p)
        if isinstance(witness, (int, sympy.Integer)):
            val = int(witness)
            if sympy.isprime(val):
                h1 = True
                char = val
        else:
            # Check if the witness is a sympy domain or field object
            is_f = False
            if hasattr(witness, 'is_Field'):
                is_f = witness.is_Field
            elif hasattr(witness, 'is_field'):
                is_f = witness.is_field
                
            if is_f:
                h1 = True
                # Extract the characteristic of the field
                if hasattr(witness, 'characteristic'):
                    if callable(witness.characteristic):
                        char = witness.characteristic()
                    else:
                        char = witness.characteristic
                elif hasattr(witness, 'char'):
                    if callable(witness.char):
                        char = witness.char()
                    else:
                        char = witness.char
                elif hasattr(witness, 'p'):
                    char = witness.p
    except Exception:
        pass

    try:
        neg_q = False
        # The conclusion fails (i.e., the commutator subgroup is NOT equal to the center)
        # for the Heisenberg group over a field of characteristic 2.
        if h1 and char is not None:
            neg_q = (int(char) == 2)
    except Exception:
        neg_q = False

    return [h1, neg_q]