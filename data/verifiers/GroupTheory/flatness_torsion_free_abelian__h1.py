import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# A standard torsion-free non-abelian group (Free group on 2 generators)
try:
    F2 = sympy.combinatorics.free_group("x y")[0]
except Exception:
    F2 = None

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the conjecture:
    "G is a flat Z-module if and only if G is a torsion-free group."
    
    A Z-module is by definition an abelian group. 
    Therefore, "G is a flat Z-module" implies G is abelian.
    The conjecture fails if G is torsion-free but NOT abelian.
    """
    try:
        is_tf = False
        is_ab = False
        
        # Determine if the group is torsion-free
        if hasattr(witness, 'is_torsion_free'):
            is_tf = witness.is_torsion_free
        elif type(witness).__name__ == 'FreeGroup':
            is_tf = True
        elif hasattr(witness, 'order'):
            order = witness.order() if callable(witness.order) else witness.order
            is_tf = (order == 1)
            
        # Determine if the group is abelian
        if hasattr(witness, 'is_abelian'):
            is_ab = witness.is_abelian
            if callable(is_ab):
                is_ab = is_ab()
        elif type(witness).__name__ == 'FreeGroup':
            is_ab = len(witness.generators) <= 1
            
        # The conclusion fails if G is torsion-free but not abelian
        # (since it cannot be a Z-module, let alone a flat one)
        neg_q = bool(is_tf and not is_ab)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: G is a torsion-free group but not a flat Z-module (i.e., G is not abelian)"
]

N_HYP = 0
NEG_Q_INDEX = 0