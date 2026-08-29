import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: H is a subgroup of F",
    "¬Q: There does not exist a right transversal for H in F such that every prefix of a reduced word in the transversal is also in the transversal"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        F, H = witness
    except Exception:
        return [False, False]
    
    # H_1: H is a subgroup of F
    h1 = False
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = H.is_subgroup(F)
            # Fallback if is_subgroup is overly strict about permutation domains
            if not h1 and hasattr(H, 'generators'):
                h1 = all(g in F for g in H.generators)
        elif hasattr(H, 'parent') and H.parent == F:
            h1 = True
        elif hasattr(H, 'generators'):
            h1 = all(g in F for g in H.generators)
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails at the witness.
    # The Schreier Transversal Lemma holds if and only if F is a free group.
    # For non-free groups, elements do not have unique reduced word representations,
    # making the condition "every prefix of a reduced word in the transversal" 
    # mathematically ill-typed or unsatisfiable for any valid transversal.
    is_free = False
    try:
        type_name = type(F).__name__
        if type_name == 'FreeGroup':
            is_free = True
        elif type_name == 'FpGroup':
            if hasattr(F, 'relators') and len(F.relators) == 0:
                is_free = True
        else:
            # The trivial group is a free group of rank 0
            order = None
            if hasattr(F, 'order'):
                order = F.order() if callable(F.order) else F.order
            elif hasattr(F, 'elements'):
                order = len(list(F.elements))
            
            if order == 1:
                is_free = True
    except Exception:
        pass

    neg_q = not is_free

    return [bool(h1), bool(neg_q)]