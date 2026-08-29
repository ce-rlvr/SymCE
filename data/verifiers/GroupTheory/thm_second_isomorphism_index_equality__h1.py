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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = bool(H.is_subgroup(G))
    except Exception:
        h1 = False

    try:
        h2 = bool(N.is_normal(G))
    except Exception:
        h2 = False

    try:
        H_elems = set(H.elements)
        N_elems = set(N.elements)
        H_cap_N_elems = H_elems.intersection(N_elems)
        if len(H_cap_N_elems) > 0:
            index_H = len(H_elems) // len(H_cap_N_elems)
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        H_elems = set(H.elements)
        N_elems = set(N.elements)
        HN_elements = {h * n for h in H_elems for n in N_elems}
        
        is_subgroup_HN = True
        for x in HN_elements:
            for y in HN_elements:
                if x * y not in HN_elements:
                    is_subgroup_HN = False
                    break
            if not is_subgroup_HN:
                break
                
        if not is_subgroup_HN:
            neg_q = True
        elif len(HN_elements) % len(N_elems) != 0:
            neg_q = True
        else:
            index_HN = len(HN_elements) // len(N_elems)
            H_cap_N_elems = H_elems.intersection(N_elems)
            index_H = len(H_elems) // len(H_cap_N_elems)
            neg_q = bool(index_HN != index_H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: N is a normal subgroup of G",
    "H_3: The index of H intersection N in H is finite",
    "not Q: The index of N in HN is not finite or not equal to the index of H intersection N in H"
]

N_HYP = 3
NEG_Q_INDEX = 3