import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential witness expressions
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

def is_infinite_cyclic(A):
    """Helper to determine if A represents an infinite cyclic group."""
    if type(A).__name__ == 'FreeGroup':
        return len(A.generators) == 1
        
    if type(A).__name__ == 'FpGroup':
        if len(A.generators) == 1 and len(A.relators) == 0:
            return True
            
    if type(A).__name__ == 'FreeGroupElement':
        return not getattr(A, 'is_identity', False)
        
    if A == sympy.S.Integers:
        return True
        
    if hasattr(A, 'order'):
        try:
            if A.order() != sympy.oo:
                return False
        except Exception:
            pass
            
    if isinstance(A, (list, tuple, set)):
        if len(A) == 0:
            return False
            
        # If A is a collection of FreeGroup elements, they generate an infinite cyclic group
        # if and only if they are all powers of the same element (i.e., they pairwise commute)
        # and at least one is non-identity.
        if not all(type(x).__name__ == 'FreeGroupElement' for x in A):
            return False
            
        non_id = [x for x in A if not getattr(x, 'is_identity', False)]
        if len(non_id) == 0:
            return False
            
        try:
            for x, y in itertools.combinations(non_id, 2):
                if x * y != y * x:
                    return False
            return True
        except Exception:
            return False
            
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok]
    """
    # Unpack witness
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            A = witness.get('A')
        elif isinstance(witness, tuple):
            if len(witness) >= 2:
                F, A = witness[0], witness[1]
            else:
                F = witness[0]
                A = witness[0]
        else:
            F = witness
            A = witness
    except Exception:
        F, A = None, None

    # H_1: F is a free group
    try:
        h1 = False
        if type(F).__name__ == 'FreeGroup':
            h1 = True
        elif type(F).__name__ == 'FpGroup' and len(F.relators) == 0:
            h1 = True
    except Exception:
        h1 = False

    # neg_Q: A is NOT an infinite cyclic group
    try:
        neg_q = not is_infinite_cyclic(A)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: A is not an infinite cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1