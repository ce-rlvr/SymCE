import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    Check if the witness is a counterexample to the conjecture.
    The true theorem is "Direct Product of Reduced Abelian Groups".
    The conjecture drops the "Abelian" hypothesis.
    Thus, a valid counterexample is a non-Abelian group (or a collection containing one),
    for which the equivalence regarding reduced groups fails in this context.
    """
    try:
        if isinstance(witness, (list, tuple, set)):
            is_abelian = all(getattr(g, 'is_abelian', True) for g in witness)
        else:
            is_abelian = getattr(witness, 'is_abelian', True)
            
        neg_q = not bool(is_abelian)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The direct product is a reduced group iff all factors are reduced"
]

N_HYP = 0
NEG_Q_INDEX = 0