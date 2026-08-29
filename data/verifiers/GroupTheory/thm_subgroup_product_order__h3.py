import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            K = witness.get('K')
        else:
            G, H, K = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: H is a finite subgroup of G
    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            # Check if all generators of H are in G, which implies H is a subgroup
            h2_ok = all(g in G for g in H.generators)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The cardinality of HK is NOT equal to (|H| * |K|) / |H \cap K|
    try:
        if isinstance(H, PermutationGroup):
            H_elems = set(H.generate_dimino())
        else:
            H_elems = set(H)
            
        if isinstance(K, PermutationGroup):
            K_elems = set(K.generate_dimino())
        else:
            K_elems = set(K)
            
        HK = set()
        for h in H_elems:
            for k in K_elems:
                HK.add(h * k)
                
        H_cap_K = H_elems.intersection(K_elems)
        
        if len(H_cap_K) == 0:
            neg_q_ok = True
        else:
            expected = (len(H_elems) * len(K_elems)) / len(H_cap_K)
            neg_q_ok = (len(HK) != expected)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a finite subgroup of G",
    "¬Q: |HK| != (|H| * |K|) / |H \\cap K|"
]

N_HYP = 2
NEG_Q_INDEX = 2