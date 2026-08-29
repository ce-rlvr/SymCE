import sympy
from sympy.combinatorics import free_group
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
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, a, b) where F is a free group, and 
    a, b are elements of F generating the maximal cyclic subgroups A and B.
    """
    try:
        F, a, b = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False

    # H_2: A and B are maximal cyclic subgroups of F
    try:
        def is_maximal_cyclic_generator(g, F):
            if not hasattr(g, 'group') or g.group != F:
                return False
            if getattr(g, 'is_identity', False):
                return False
            
            try:
                arr = list(g.array_form)
            except Exception:
                return False
            
            # Cyclically reduce the word
            while len(arr) > 1 and arr[0][0] == arr[-1][0]:
                if arr[0][1] + arr[-1][1] == 0:
                    arr.pop(0)
                    arr.pop(-1)
                else:
                    arr[0] = (arr[0][0], arr[0][1] + arr[-1][1])
                    arr.pop(-1)
                    break
                    
            if len(arr) == 0:
                return False
            if len(arr) == 1:
                return abs(arr[0][1]) == 1
            
            # Check if the cyclically reduced word is a proper power
            for k in range(1, len(arr) // 2 + 1):
                if len(arr) % k == 0:
                    if arr == arr[:k] * (len(arr) // k):
                        return False
            return True

        h2 = is_maximal_cyclic_generator(a, F) and is_maximal_cyclic_generator(b, F)
    except Exception:
        h2 = False

    # ¬Q: The intersection of A and B is not the trivial subgroup
    try:
        # In a free group, the intersection of two maximal cyclic subgroups <a> and <b>
        # is non-trivial if and only if they are the exact same subgroup.
        # Since a and b are generators of maximal cyclic subgroups, 
        # <a> = <b> if and only if a == b or a == b**-1.
        neg_q = (a == b) or (a == b**-1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: A and B are maximal cyclic subgroups of F",
    "¬Q: The intersection of A and B is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2