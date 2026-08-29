import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, S, N = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: S is a subset of G that generates G
    try:
        if all(s in G for s in S):
            S_list = list(S)
            if not S_list:
                h2 = (G.order() == 1)
            else:
                H = PermutationGroup(S_list)
                h2 = (H.order() == G.order())
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The set of cosets {sN | s \in S} does NOT generate the quotient group G/N
    try:
        if isinstance(N, PermutationGroup):
            N_group = N
            is_valid_subgroup = N_group.is_subgroup(G)
        else:
            N_list = list(N)
            if not N_list:
                N_group = None
                is_valid_subgroup = False
            else:
                N_group = PermutationGroup(N_list)
                unique_N = set(N_list)
                # Check if N is actually a subgroup, not just a subset that generates one
                if len(unique_N) != N_group.order():
                    is_valid_subgroup = False
                else:
                    is_valid_subgroup = N_group.is_subgroup(G)
                    
        if not is_valid_subgroup:
            is_normal = False
        else:
            is_normal = N_group.is_normal(G)
            
        if not is_normal:
            # If N is not a normal subgroup, G/N is not a quotient group, so the conclusion fails.
            neg_q = True
        else:
            # If N is a normal subgroup, check if {sN | s \in S} generates G/N.
            # This is true if and only if S \cup N generates G.
            S_list = list(S)
            N_gens = N_group.generators
            combined_gens = S_list + N_gens
            if not combined_gens:
                generates_quotient = (G.order() == 1)
            else:
                combined_group = PermutationGroup(combined_gens)
                generates_quotient = (combined_group.order() == G.order())
            neg_q = not generates_quotient
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: S is a subset of G that generates G",
    "¬Q: The set of cosets {sN | s in S} does not generate the quotient group G/N"
]

N_HYP = 2
NEG_Q_INDEX = 2