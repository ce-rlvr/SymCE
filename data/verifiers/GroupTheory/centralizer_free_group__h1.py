import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        F, x = witness
    except Exception:
        return [False, False]
        
    # H_1: x is an element of F such that x is not the identity
    try:
        try:
            in_F = x in F
        except Exception:
            in_F = F.contains(x)
            
        try:
            is_not_id = (x != F.identity)
        except Exception:
            is_not_id = not x.is_identity
            
        h1 = bool(in_F and is_not_id)
    except Exception:
        h1 = False
        
    # ¬Q: C_F(x) is not an infinite cyclic group
    try:
        if isinstance(F, PermutationGroup):
            # Any PermutationGroup in sympy is finite. 
            # A finite group cannot have an infinite cyclic subgroup.
            neg_q = True
        elif type(F).__name__ == 'FreeGroup':
            # In a FreeGroup, the centralizer of a non-identity element IS infinite cyclic.
            if len(F.generators) == 1:
                neg_q = False
            else:
                try:
                    is_id = (x == F.identity)
                except Exception:
                    is_id = x.is_identity
                
                if is_id:
                    # The centralizer of the identity is the whole group, which is not cyclic if rank > 1
                    neg_q = True
                else:
                    # The centralizer of a non-identity element in a free group is infinite cyclic
                    neg_q = False
        else:
            # Fallback for other types (e.g. FpGroup), assuming finite counterexamples are provided
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of F such that x is not the identity",
    "¬Q: C_F(x) is not an infinite cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1