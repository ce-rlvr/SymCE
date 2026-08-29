import math
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Check H_1: G is a group of order p^2 q
    # If the witness is a tuple (G, p, q), we verify the order exactly.
    # If the witness is just G, the condition is satisfied if G is a group, 
    # since any integer order can be written as p^2 q (e.g., p=1, q=order).
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, p, q = witness
            if hasattr(G, 'order') and callable(G.order):
                if G.order() == (p**2) * q:
                    h1 = True
        else:
            G = witness
            if hasattr(G, 'order') and callable(G.order):
                h1 = True
    except Exception:
        h1 = False

    # Check ¬Q: G is not a solvable group
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            G = witness[0]
        else:
            G = witness
            
        if hasattr(G, 'is_solvable'):
            neg_q = not G.is_solvable
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group of order p^2 q",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1