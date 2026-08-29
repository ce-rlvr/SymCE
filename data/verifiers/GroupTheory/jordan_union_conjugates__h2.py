import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            G = witness
            H = witness
            
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(H, PermutationGroup) and 
              H.is_subgroup(G))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            G = witness
            H = witness
            
        G_elements = list(G.generate())
        H_elements = list(H.generate())
        
        union_conjugates = set()
        for g in G_elements:
            g_inv = ~g
            for h in H_elements:
                union_conjugates.add(g * h * g_inv)
                
        neg_q = len(union_conjugates) >= len(G_elements)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and H is a subgroup of G",
    "¬Q: The union of all conjugates of H in G is not strictly a proper subset of G"
]

N_HYP = 1
NEG_Q_INDEX = 1