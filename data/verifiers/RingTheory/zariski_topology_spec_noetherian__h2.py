import sympy
from sympy import ZZ, QQ
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Returns [H_1_ok, neg_Q_ok].
    """
    # H_1: Let R be a commutative Noetherian ring.
    try:
        is_comm = getattr(witness, 'is_commutative', True)
        
        is_noeth = False
        if hasattr(witness, 'is_noetherian'):
            is_noeth = bool(witness.is_noetherian)
        elif hasattr(witness, 'is_Domain') and witness.is_Domain:
            if witness in (ZZ, QQ):
                is_noeth = True
            elif hasattr(witness, 'is_Field') and witness.is_Field:
                is_noeth = True
            elif hasattr(witness, 'domain') and hasattr(witness, 'gens'):
                # Finite polynomial rings over Noetherian domains in sympy
                is_noeth = True
            else:
                is_noeth = False
        else:
            is_noeth = False
            
        h1 = bool(is_comm and is_noeth)
    except Exception:
        h1 = False

    # neg_Q: The topological space Spec(R) is NOT a Noetherian space.
    try:
        is_spec_noeth = False
        if hasattr(witness, 'is_spec_noetherian'):
            is_spec_noeth = bool(witness.is_spec_noetherian)
        elif is_noeth:
            # A standard theorem states that if R is Noetherian, Spec(R) is a Noetherian space.
            is_spec_noeth = True
            
        neg_q = not is_spec_noeth
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: The topological space Spec(R) is not a Noetherian space"
]

N_HYP = 1
NEG_Q_INDEX = 1