import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
        # Implicitly require H to be a subset of G for the witness to be well-formed
        if h1_ok:
            elements = set(G.generate())
            if isinstance(H, PermutationGroup):
                H_list = list(H.generate())
            else:
                H_list = list(H)
            if not all(isinstance(h, Permutation) and h in elements for h in H_list):
                h1_ok = False
    except Exception:
        h1_ok = False

    # neg_Q: The collection of all left cosets {gH | g \in G} does NOT form a partition of G
    try:
        elements = set(G.generate())
        if isinstance(H, PermutationGroup):
            H_list = list(H.generate())
        else:
            H_list = list(H)
            
        cosets = set()
        for g in elements:
            coset = frozenset(g * h for h in H_list)
            cosets.add(coset)
            
        union = set()
        sum_sizes = 0
        has_empty = False
        for c in cosets:
            if not c:
                has_empty = True
            union.update(c)
            sum_sizes += len(c)
            
        # A collection of sets is a partition of G if:
        # 1. It does not contain the empty set
        # 2. The union of all sets is exactly G
        # 3. The sets are mutually disjoint (sum of sizes equals size of union)
        is_partition = (not has_empty) and (union == elements) and (sum_sizes == len(elements))
        neg_q_ok = not is_partition
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The collection of all left cosets {gH | g in G} does not form a partition of G"
]

N_HYP = 1
NEG_Q_INDEX = 1