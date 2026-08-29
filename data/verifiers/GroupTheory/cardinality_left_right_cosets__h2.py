import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for witness expressions
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # ¬Q: There is no bijection between the set of left cosets of H in G and the set of right cosets of H in G
    try:
        if not h1:
            neg_q = False
        else:
            # Restrict to reasonably sized finite groups to ensure fast execution
            if G.order() > 1000:
                neg_q = False
            else:
                H_list = list(H)
                if len(H_list) > 1000:
                    neg_q = False
                else:
                    left_cosets = set()
                    right_cosets = set()
                    
                    for g in G.elements:
                        l_coset = frozenset([g * h for h in H_list])
                        r_coset = frozenset([h * g for h in H_list])
                        left_cosets.add(l_coset)
                        right_cosets.add(r_coset)
                        
                    # If the number of distinct left cosets differs from the number of distinct right cosets,
                    # there can be no bijection between them (since the sets are finite).
                    neg_q = len(left_cosets) != len(right_cosets)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: There is no bijection between the set of left cosets of H in G and the set of right cosets of H in G"
]

N_HYP = 1
NEG_Q_INDEX = 1