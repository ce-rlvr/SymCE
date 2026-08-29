import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    # H_1: G is not an abelian group
    try:
        if hasattr(witness, 'is_abelian'):
            is_ab = witness.is_abelian
            if is_ab is None:
                is_ab = False
            else:
                is_ab = bool(is_ab)
        elif hasattr(witness, 'is_Abelian'):
            is_ab = witness.is_Abelian
            if is_ab is None:
                is_ab = False
            else:
                is_ab = bool(is_ab)
        else:
            # If it lacks the property, it is not a SymPy group object.
            is_ab = False
        h1 = not is_ab
    except Exception:
        h1 = False

    # neg_Q: The number of pairs (x, y) in G x G such that xy = yx is strictly greater than (5/8) * |G|^2
    try:
        if hasattr(witness, 'elements'):
            iterable = witness.elements
        else:
            iterable = witness
            
        elements = []
        for i, x in enumerate(iterable):
            # Cap the size to prevent timeouts on infinite or very large structures
            if i >= 200:
                return [h1, False]
            elements.append(x)
            
        n = len(elements)
        if n == 0:
            return [h1, False]
            
        pairs = 0
        for x in elements:
            for y in elements:
                if x * y == y * x:
                    pairs += 1
                    
        neg_q = pairs > (5 / 8) * (n ** 2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is not an abelian group",
    "¬Q: The number of commuting pairs is strictly greater than (5/8) * |G|^2"
]

N_HYP = 1
NEG_Q_INDEX = 1