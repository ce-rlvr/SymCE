import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        
    # H1: N is a normal subgroup of G
    try:
        if hasattr(N, 'is_normal'):
            h1 = bool(N.is_subgroup(G) and N.is_normal(G))
        else:
            N_elements = []
            for item in N:
                if isinstance(item, Permutation):
                    N_elements.append(item)
                else:
                    N_elements.append(Permutation(item))
            N_group = PermutationGroup(N_elements)
            # Check if N is exactly the subgroup it generates (i.e., it is closed and contains identity)
            if N_group.order() != len(set(N_elements)):
                h1 = False
            else:
                h1 = bool(N_group.is_subgroup(G) and N_group.is_normal(G))
    except Exception:
        h1 = False
        
    # neg_Q: N is NOT a disjoint union of conjugacy classes of G
    try:
        if hasattr(N, 'generate'):
            n_elements = set(N.generate())
        else:
            n_elements = set()
            for item in N:
                if isinstance(item, Permutation):
                    n_elements.add(item)
                else:
                    n_elements.add(Permutation(item))
            
        # Check if N is a subset of G
        is_subset = True
        for n in n_elements:
            if n not in G:
                is_subset = False
                break
                
        if not is_subset:
            is_union_of_cc = False
        else:
            # N is a union of conjugacy classes of G iff it is closed under conjugation by G.
            # It suffices to check closure under conjugation by the generators of G.
            is_union_of_cc = True
            for n in n_elements:
                for g in G.generators:
                    conj = g * n * (~g)
                    if conj not in n_elements:
                        is_union_of_cc = False
                        break
                if not is_union_of_cc:
                    break
                    
        neg_q = not is_union_of_cc
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: N is not a disjoint union of conjugacy classes of G"
]

N_HYP = 1
NEG_Q_INDEX = 1