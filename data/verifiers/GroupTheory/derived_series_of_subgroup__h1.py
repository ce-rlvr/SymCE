import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
            n = witness.get('n')
        else:
            G, H, n = witness
    except Exception:
        return [False, False, False]

    # H_1: H is a subgroup of G
    try:
        h1 = (hasattr(H, 'generators') and 
              hasattr(G, '__contains__') and 
              all(g in G for g in H.generators))
    except Exception:
        h1 = False

    # H_2: n is a non-negative integer
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and int(n) >= 0
    except Exception:
        h2 = False

    # ¬Q: The n-th derived subgroup H^(n) is NOT a subgroup of the n-th derived subgroup G^(n)
    try:
        n_int = int(n)
        H_n = H
        for _ in range(n_int):
            H_n = H_n.derived_subgroup()
            
        G_n = G
        for _ in range(n_int):
            G_n = G_n.derived_subgroup()
            
        is_subgroup = (hasattr(H_n, 'generators') and 
                       hasattr(G_n, '__contains__') and 
                       all(g in G_n for g in H_n.generators))
        neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: n is a non-negative integer",
    "¬Q: H^(n) is not a subgroup of G^(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2