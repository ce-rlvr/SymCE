import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is finitely generated
    try:
        h1 = isinstance(G, PermutationGroup) or (hasattr(G, 'generators') and len(G.generators) >= 0)
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        h2 = H.is_subgroup(G)
    except Exception:
        h2 = False
        
    # neg_Q: The quotient group G/H is not finitely generated
    try:
        # The quotient G/H is a well-defined group iff H is a normal subgroup of G.
        # Since G is finitely generated, if G/H is a group, it is automatically finitely generated.
        # Therefore, the conclusion "G/H is a finitely generated group" fails iff H is not normal in G.
        neg_q = not G.is_normal(H)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is finitely generated",
    "H_2: H is a subgroup of G",
    "¬Q: The quotient group G/H is not finitely generated (or not a well-defined group)"
]

N_HYP = 2
NEG_Q_INDEX = 2