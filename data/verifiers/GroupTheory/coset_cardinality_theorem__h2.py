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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        G, H, x = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1_ok = bool(isinstance(G, PermutationGroup))
    except Exception:
        h1_ok = False
        
    # H_2: x is an element of G
    try:
        if hasattr(G, 'contains'):
            h2_ok = bool(G.contains(x))
        else:
            h2_ok = bool(x in G.elements)
    except Exception:
        h2_ok = False
        
    # neg_Q: The conclusion fails
    # The conclusion states "The cardinality of the left coset xH is equal to the cardinality of H".
    # This presupposes that xH is a valid left coset, which requires H to be a subgroup of G.
    # If H is not a subgroup, the conclusion is false.
    try:
        if isinstance(H, PermutationGroup):
            H_elements = list(H.elements)
        else:
            H_elements = list(H)
            
        is_subset = True
        for h in H_elements:
            try:
                if not G.contains(h):
                    is_subset = False
                    break
            except Exception:
                is_subset = False
                break
                
        if not is_subset:
            is_sub = False
        else:
            try:
                if G.identity not in H_elements:
                    is_sub = False
                else:
                    is_sub = True
                    for a in H_elements:
                        if a**-1 not in H_elements:
                            is_sub = False
                            break
                        for b in H_elements:
                            if a * b not in H_elements:
                                is_sub = False
                                break
            except Exception:
                is_sub = False
                            
        try:
            unique_H = set(H_elements)
            xH = set(x * h for h in unique_H)
            card_equal = (len(xH) == len(unique_H))
        except Exception:
            card_equal = False
            
        conclusion_holds = is_sub and card_equal
        neg_q_ok = not conclusion_holds
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "¬Q: The cardinality of the left coset xH is not equal to the cardinality of H (or xH is not a valid left coset)"
]

N_HYP = 2
NEG_Q_INDEX = 2