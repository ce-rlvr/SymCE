import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

class Presentation:
    """
    Represents a group presentation.
    group_id: an identifier for the isomorphism class of the group (e.g., 'Z', 'trivial')
    generators: number of generators (can be math.inf for infinite)
    relators: number of relators (can be math.inf for infinite)
    """
    def __init__(self, group_id, generators, relators):
        self.group_id = group_id
        self.generators = float(generators)
        self.relators = float(relators)

# Standard group theory and linear algebra objects
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
    try:
        P1, P2 = witness
        
        # H_1: The group defined by P_1 is isomorphic to the group defined by P_2.
        h1 = (P1.group_id == P2.group_id)
        
        # ¬Q: The presentation P_1 CANNOT be transformed into the presentation P_2 
        # by applying a finite sequence of Tietze transformations.
        # A finite sequence of Tietze transformations can only change the number of 
        # generators and relators by a finite amount. If one presentation is finite 
        # and the other is infinite, they cannot be transformed into each other.
        def is_finite(p):
            return p.generators != float('inf') and p.relators != float('inf')
            
        if is_finite(P1) and is_finite(P2):
            # If both are finite, Tietze's Equivalence Theorem guarantees they CAN be 
            # transformed into each other (since they define isomorphic groups).
            # Thus the conclusion holds, and its negation is False.
            neg_q = False
        else:
            # If at least one presentation is infinite, they generally cannot be 
            # transformed into each other by a finite sequence of Tietze transformations.
            # This provides the counterexample to the false conjecture.
            neg_q = True
            
    except Exception:
        h1 = False
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The group defined by P_1 is isomorphic to the group defined by P_2",
    "¬Q: P_1 cannot be transformed into P_2 by a finite sequence of Tietze transformations"
]

N_HYP = 1
NEG_Q_INDEX = 1