import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if isinstance(witness, dict):
            G = witness['G']
            A = witness['A']
            B = witness['B']
        else:
            G, A, B = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a permutation group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: A and B are subsets of X (the domain of G, represented by non-negative integers)
    try:
        A_set = set(A)
        B_set = set(B)
        h2 = all(isinstance(x, (int, sympy.Integer)) and x >= 0 for x in A_set.union(B_set))
    except Exception:
        h2 = False
        
    # ¬Q: The pointwise stabilizer G_{(A \cup B)} is NOT equal to G_{(A)} \cap G_{(B)}
    try:
        def pointwise_stabilizer(group, S):
            S_set = {int(x) for x in S}
            # A permutation g is in the pointwise stabilizer if it fixes every element in S
            return set(g for g in group.elements if all(g(x) == x for x in S_set))
            
        stab_A = pointwise_stabilizer(G, A_set)
        stab_B = pointwise_stabilizer(G, B_set)
        stab_A_cup_B = pointwise_stabilizer(G, A_set.union(B_set))
        
        neg_q = stab_A_cup_B != stab_A.intersection(stab_B)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a permutation group",
    "H_2: A and B are subsets of X",
    "¬Q: G_{(A \\cup B)} != G_{(A)} \\cap G_{(B)}"
]

N_HYP = 2
NEG_Q_INDEX = 2