import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        # The conclusion states: "The center Z(G) has order 2 and consists of the elements 1 and -1."
        # We interpret "consists of 1 and -1" as the group having a unique element of order 2,
        # which acts as "-1" (as is the case in the Quaternion group Q8).
        center = witness.center()
        
        if center.order() != 2:
            neg_q = True
        else:
            if hasattr(witness, 'elements'):
                # Check if there is exactly one element of order 2 in the entire group
                order_2_elements = [g for g in witness.elements if g.order() == 2]
                neg_q = (len(order_2_elements) != 1)
            else:
                # Fallback if elements cannot be iterated
                neg_q = False
                
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The center Z(G) does not have order 2 or does not consist of 1 and -1"
]

N_HYP = 0
NEG_Q_INDEX = 0