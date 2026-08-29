import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, oo

# Standard finite groups
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

# Standard matrices
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# Helper class for infinite abelian groups (e.g., the integers Z)
class InfiniteAbelianGroup:
    @property
    def is_abelian(self):
        return True
    
    @property
    def is_finite(self):
        return False
        
    def order(self):
        return sympy.oo
        
    def __mul__(self, other):
        return self
        
    def __pow__(self, n):
        return self

Z = InfiniteAbelianGroup()
Z_group = Z

def conditions(witness) -> list[bool]:
    # H_1: G is an abelian group
    try:
        h1 = False
        if hasattr(witness, 'is_abelian'):
            val = witness.is_abelian() if callable(witness.is_abelian) else witness.is_abelian
            h1 = bool(val)
        elif type(witness).__name__ == 'FreeGroup':
            # A free group is abelian iff its rank is <= 1
            h1 = (len(witness.generators) <= 1)
    except Exception:
        h1 = False

    # H_2: C* is the multiplicative group of non-zero complex numbers
    # This is a domain context fact that is universally true.
    h2 = True

    # ¬Q: G is NOT isomorphic to the group of all group homomorphisms from G to C*
    # For abelian groups, G is isomorphic to its character group iff G is finite.
    # Therefore, the conclusion fails (¬Q is True) iff G is infinite.
    try:
        is_fin = True  # Default to True so neg_Q is False unless we can prove it's infinite
        if hasattr(witness, 'order'):
            ord_G = witness.order() if callable(witness.order) else witness.order
            if ord_G == sympy.oo:
                is_fin = False
            elif isinstance(ord_G, (int, sympy.Integer)):
                is_fin = True
        elif hasattr(witness, 'is_finite'):
            val = witness.is_finite() if callable(witness.is_finite) else witness.is_finite
            is_fin = bool(val)
        elif type(witness).__name__ == 'FreeGroup':
            is_fin = (len(witness.generators) == 0)
            
        neg_q = not is_fin
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: C* is the multiplicative group of non-zero complex numbers",
    "¬Q: G is not isomorphic to the group of all group homomorphisms from G to C*"
]

N_HYP = 2
NEG_Q_INDEX = 2