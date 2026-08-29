import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture:
    "G is a divisible group if and only if G is an injective object in the category of abelian groups."
    
    A counterexample must be a group where this biconditional fails.
    Since injective objects in Ab must be abelian, a divisible non-abelian group
    satisfies the LHS (is divisible) but fails the RHS (is not in Ab, so not injective in Ab).
    """
    try:
        # Check if witness is abelian
        if hasattr(witness, 'is_abelian'):
            if callable(witness.is_abelian):
                abelian = bool(witness.is_abelian())
            else:
                abelian = bool(witness.is_abelian)
        else:
            abelian = False
            
        # Check if witness is divisible
        if hasattr(witness, 'is_divisible'):
            if callable(witness.is_divisible):
                divisible = bool(witness.is_divisible())
            else:
                divisible = bool(witness.is_divisible)
        elif hasattr(witness, 'order'):
            # For finite groups, only the trivial group is divisible
            divisible = (witness.order() == 1)
        else:
            divisible = False
            
        # An injective object in the category of abelian groups must be both abelian and divisible
        injective_in_ab = abelian and divisible
        
        # The conjecture claims: divisible <-> injective_in_ab
        conclusion = (divisible == injective_in_ab)
        
        # The negated conclusion is True when the conjecture's biconditional fails
        neg_q = not conclusion
        
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G is a divisible group but not an injective object in the category of abelian groups (or vice versa)"
]

N_HYP = 0
NEG_Q_INDEX = 0