import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness):
    try:
        G, N, H = witness
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(N, PermutationGroup) and 
              isinstance(H, PermutationGroup))
        if h1:
            G_elems = set(G.generate_dimino())
            h1 = (all(g in G_elems for g in N.generators) and 
                  all(g in G_elems for g in H.generators))
    except Exception:
        h1 = False

    try:
        G, N, H = witness
        
        H_set = set(H.generate_dimino())
        G_elems = list(G.generate_dimino())
        N_elems = list(N.generate_dimino())
        
        # K = normal core of H in G
        # K = { x \in H | g * x * g^-1 \in H for all g \in G }
        K_elements = set()
        for x in H_set:
            if all((g * x * ~g) in H_set for g in G_elems):
                K_elements.add(x)
                
        # C_H(N) = centralizer of N in H
        # C_H(N) = { h \in H | h * n == n * h for all n \in N }
        C_H_N_elements = set()
        for h in H_set:
            if all(h * n == n * h for n in N_elems):
                C_H_N_elements.add(h)
                
        neg_q = K_elements != C_H_N_elements
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group, N and H are subgroups of G",
    "¬Q: The normal core K is not equal to the centralizer C_H(N)"
]

N_HYP = 1
NEG_Q_INDEX = 1