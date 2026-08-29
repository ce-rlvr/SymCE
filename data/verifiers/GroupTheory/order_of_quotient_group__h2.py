import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup

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

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        try:
            # Attempt to compute the quotient group and check its order.
            # If N is not a normal subgroup, quotient_group may raise an exception,
            # or it may return a group whose order is not |G| / |N|.
            # In either case, the conclusion fails.
            q_group = G.quotient_group(N)
            q_order = q_group.order()
            conclusion = (G.order() == q_order * N.order())
        except Exception:
            conclusion = False
            
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The order of the quotient group G/N is not equal to |G| / |N| (or G/N is undefined)"
]

N_HYP = 1
NEG_Q_INDEX = 1