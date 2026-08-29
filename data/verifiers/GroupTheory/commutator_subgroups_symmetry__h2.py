import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(K, PermutationGroup) and K.is_subgroup(G)
    except Exception:
        h2_ok = False

    try:
        if isinstance(H, Permutation):
            elements_H = [H]
        elif hasattr(H, 'elements'):
            elements_H = list(H.elements)
        else:
            elements_H = list(H)
            
        if isinstance(K, Permutation):
            elements_K = [K]
        elif hasattr(K, 'elements'):
            elements_K = list(K.elements)
        else:
            elements_K = list(K)
            
        gens_HK = []
        for h in elements_H:
            for k in elements_K:
                gens_HK.append((~h) * (~k) * h * k)
                
        gens_KH = []
        for k in elements_K:
            for h in elements_H:
                gens_KH.append((~k) * (~h) * k * h)
                
        if not gens_HK:
            neg_q_ok = False
        else:
            sub_HK = PermutationGroup(gens_HK)
            sub_KH = PermutationGroup(gens_KH)
            
            if sub_HK != sub_KH:
                neg_q_ok = True
            else:
                set_HK = set(gens_HK)
                set_KH = set(gens_KH)
                neg_q_ok = (set_HK != set_KH)
                
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a subgroup of G",
    "not Q: The commutator subgroup of H and K is not equal to that of K and H"
]

N_HYP = 2
NEG_Q_INDEX = 2