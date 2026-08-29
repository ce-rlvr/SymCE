import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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
    """
    Checks if the witness is a counterexample to the conjecture:
    "X is connected if and only if the only subsets of X that are both open and closed are ∅ and X."
    
    The dropped hypothesis from the true theorem is "X is non-empty".
    By modern definitions, the empty set is NOT connected (it does not have exactly two clopen subsets).
    However, for X = ∅, the only subsets of X that are clopen are ∅, which means the set of clopen 
    subsets is {∅}. Since {∅, X} = {∅, ∅} = {∅}, the right-hand side of the equivalence is TRUE.
    Thus, LHS is False and RHS is True, making the empty set the counterexample.
    """
    try:
        is_empty = False
        if witness is sympy.S.EmptySet:
            is_empty = True
        elif hasattr(witness, 'is_EmptySet') and witness.is_EmptySet:
            is_empty = True
        elif isinstance(witness, (list, tuple, set, frozenset)) and len(witness) == 0:
            is_empty = True
            
        neg_q = bool(is_empty)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: X is the empty set (which is not connected, but satisfies the condition that its only clopen subsets are ∅ and X)"
]
N_HYP = 0
NEG_Q_INDEX = 0