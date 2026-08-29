import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup

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
            n = witness.get('n')
        else:
            G, H, n = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        n_val = int(n)
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G) and 0 <= n_val <= 1000
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            H_elems = set(H.generate())
            K_elems = set(H_elems)
            for g in G.generate():
                Hg_elems = {g * h * g**-1 for h in H_elems}
                K_elems = K_elems.intersection(Hg_elems)
                if len(K_elems) == 1:
                    break
            
            K_order = len(K_elems)
            G_order = int(G.order())
            index = G_order // K_order
            
            n_fact = math.factorial(n_val)
            neg_q = (n_fact % index != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: G is a finite group",
    "H_2: K is the normal core of H in G",
    "not_Q: The index of K in G does not divide n factorial"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2