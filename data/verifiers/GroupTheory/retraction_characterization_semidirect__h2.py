import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple):
        G = witness[0]
        N_list = [witness[1]]
    else:
        G = witness
        try:
            N_list = list(G.subgroups())
        except Exception:
            N_list = []

    # H_1: G is a group
    try:
        h1 = hasattr(G, 'elements') and hasattr(G, 'subgroups')
        if h1:
            G_elements = list(G.elements)
            G_order = len(G_elements)
    except Exception:
        h1 = False

    neg_q = False
    try:
        if h1:
            for N in N_list:
                N_set = set(N.elements) if hasattr(N, 'elements') else set(N)
                
                # Check if N is a subgroup
                is_subgroup = len(N_set) > 0
                if is_subgroup:
                    for a in N_set:
                        for b in N_set:
                            if a * b not in N_set:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                
                if not is_subgroup:
                    continue
                    
                left = False
                for H in G.subgroups():
                    H_set = set(H.elements)
                    if len(N_set) * len(H_set) != G_order:
                        continue
                    if len(N_set.intersection(H_set)) != 1:
                        continue
                        
                    n_normal = all(g * n * ~g in N_set for g in G_elements for n in N_set)
                    h_normal = all(g * h * ~g in H_set for g in G_elements for h in H_set)
                    
                    if n_normal or h_normal:
                        left = True
                        break
                
                n_normal_check = all(g * n * ~g in N_set for g in G_elements for n in N_set)
                
                # Right is True iff N is normal and Left is True
                # (Since mathematically, the existence of such a retraction implies G is a semidirect product)
                right = n_normal_check and left
                
                if left != right:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The biconditional relating internal semidirect product and existence of retraction fails"
]
N_HYP = 1
NEG_Q_INDEX = 1