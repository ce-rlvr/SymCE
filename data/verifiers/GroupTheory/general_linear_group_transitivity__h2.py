import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to represent the dimension of the vector space V.
    """
    try:
        # Extract dimension n from the witness
        if hasattr(witness, 'dimension'):
            n = int(witness.dimension)
        elif hasattr(witness, 'shape'):
            n = int(witness.shape[0])
        elif isinstance(witness, tuple):
            n = int(witness[0])
        elif isinstance(witness, list):
            n = len(witness)
        else:
            n = int(witness)
            
        # Dimension must be non-negative for a valid vector space
        if n < 0:
            return [False, False, False]
            
        # H_1: V is a finite-dimensional vector space over a field F.
        # Any non-negative integer n can represent the dimension of F^n.
        h1 = True
        
        # H_2: GL(V) is the general linear group of V.
        # This is a definitional hypothesis and holds for our model.
        h2 = True
        
        # ¬Q: The natural action of GL(V) on V \setminus {0} is NOT transitive.
        # A group action is transitive if and only if it has exactly one orbit.
        # If n == 0, V = {0}, so V \setminus {0} is the empty set.
        # The empty set has 0 orbits, hence the action is vacuously NOT transitive.
        # For n > 0, GL(V) can map any non-zero vector to any other, so it is transitive.
        neg_q = (n == 0)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: GL(V) is the general linear group of V",
    "¬Q: The natural action of GL(V) on V \\setminus {0} is not transitive"
]

N_HYP = 2
NEG_Q_INDEX = 2