import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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
        G, N, x, y = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            # Check if N is a subgroup of G
            if all(G.contains(gen) for gen in N.generators):
                # Check if N is normal in G
                is_norm = True
                for g in G.generators:
                    for n in N.generators:
                        if not N.contains(g * n * ~g):
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h2 = is_norm
    except Exception:
        h2 = False
        
    # H_3: x and y are elements of G
    try:
        h3 = isinstance(x, Permutation) and isinstance(y, Permutation) and G.contains(x) and G.contains(y)
    except Exception:
        h3 = False
        
    # ¬Q: For all n in N, x is not conjugate to yn in G
    try:
        neg_q = True
        G_elems = list(G.generate())
        N_elems = list(N.generate())
        for n in N_elems:
            target = y * n
            is_conj = False
            for g in G_elems:
                if g * x * ~g == target:
                    is_conj = True
                    break
            if is_conj:
                neg_q = False
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: x and y are elements of G",
    "¬Q: For all n in N, x is not conjugate to yn in G"
]

N_HYP = 3
NEG_Q_INDEX = 3