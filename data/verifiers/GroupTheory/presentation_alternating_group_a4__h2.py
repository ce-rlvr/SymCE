import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.free_groups import FreeGroup

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

def conditions(witness) -> list[bool]:
    # H_1: Let G be a group defined by the presentation <a, b | R>.
    try:
        h1 = isinstance(witness, (PermutationGroup, FpGroup, FreeGroup))
    except Exception:
        h1 = False

    # ¬Q: The group G is NOT isomorphic to the alternating group A_4.
    try:
        if not h1:
            neg_q = False
        else:
            is_A4 = False
            order = None
            
            if callable(getattr(witness, 'order', None)):
                order = witness.order()
            elif hasattr(witness, 'order'):
                order = witness.order
                
            if order == 12:
                checked_isomorphic = False
                if hasattr(witness, 'is_isomorphic'):
                    try:
                        is_A4 = witness.is_isomorphic(AlternatingGroup(4))
                        checked_isomorphic = True
                    except Exception:
                        pass
                
                # Fallback to element orders if is_isomorphic fails or doesn't exist
                if not checked_isomorphic and hasattr(witness, 'elements'):
                    try:
                        elements = list(witness.elements)
                        order_counts = {}
                        for g in elements:
                            o = g.order()
                            order_counts[o] = order_counts.get(o, 0) + 1
                        # A_4 is the unique group of order 12 with exactly 3 elements of order 2 and 8 of order 3
                        if order_counts.get(2, 0) == 3 and order_counts.get(3, 0) == 8:
                            is_A4 = True
                    except Exception:
                        pass
            
            neg_q = not is_A4
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group defined by the presentation <a, b | R>",
    "¬Q: G is not isomorphic to the alternating group A_4"
]

N_HYP = 1
NEG_Q_INDEX = 1