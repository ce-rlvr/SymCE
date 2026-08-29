import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import free_group
from sympy.matrices import eye, zeros

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Free groups
try:
    F1 = free_group('x')[0]
    F2 = free_group('x, y')[0]
    F3 = free_group('x, y, z')[0]
except Exception:
    F1 = None
    F2 = None
    F3 = None

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: F is a free group
    try:
        if type(witness).__name__ == 'FreeGroup':
            h1 = True
        elif type(witness).__name__ == 'FpGroup' and len(witness.relators) == 0:
            h1 = True
        elif hasattr(witness, 'is_trivial') and witness.is_trivial:
            # The trivial group is the free group of rank 0
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: Inn(F) is not isomorphic to F
    try:
        if type(witness).__name__ == 'FreeGroup':
            # For a free group F, Inn(F) ~ F/Z(F).
            # Z(F) is trivial if rank > 1, and Z(F) = F if rank <= 1.
            # Thus, Inn(F) is isomorphic to F iff rank != 1.
            # So Inn(F) is NOT isomorphic to F iff rank == 1.
            neg_q = (witness.rank == 1)
        elif type(witness).__name__ == 'FpGroup' and len(witness.relators) == 0:
            neg_q = (len(witness.generators) == 1)
        elif hasattr(witness, 'is_trivial') and witness.is_trivial:
            # Trivial group: Inn(F) is trivial, F is trivial. They are isomorphic.
            neg_q = False
        else:
            # For finite groups, Inn(G) ~ G/Z(G).
            # Inn(G) is isomorphic to G iff Z(G) is trivial.
            # So Inn(G) is NOT isomorphic to G iff Z(G) is not trivial.
            if hasattr(witness, 'center'):
                if callable(witness.center):
                    Z = witness.center()
                else:
                    Z = witness.center
                
                if hasattr(Z, 'is_trivial'):
                    neg_q = not Z.is_trivial
                elif hasattr(Z, 'order'):
                    if callable(Z.order):
                        neg_q = (Z.order() > 1)
                    else:
                        neg_q = (Z.order > 1)
                else:
                    neg_q = False
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: Inn(F) is not isomorphic to F"
]

N_HYP = 1
NEG_Q_INDEX = 1