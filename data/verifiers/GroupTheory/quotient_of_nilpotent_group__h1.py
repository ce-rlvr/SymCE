import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup

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

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    # H_1: Let N be a normal subgroup of G.
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(N, PermutationGroup) and 
              N.is_subgroup(G) and 
              G.is_normal(N))
    except Exception:
        h1 = False
        
    # ¬Q: The quotient group G/N is NOT a nilpotent group.
    # A quotient group G/N is nilpotent if and only if the lower central series of G 
    # eventually falls into N. We check if the stable term of the lower central series 
    # of G is a subgroup of N.
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)):
            neg_q = False
        else:
            lcs = G.lower_central_series()
            last_L = lcs[-1]
            is_nilp = last_L.is_subgroup(N)
            neg_q = not is_nilp
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: G/N is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1