import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
        G, H, K, x = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: K is a subgroup of G
    try:
        h2_ok = isinstance(K, PermutationGroup) and K.is_subgroup(G)
    except Exception:
        h2_ok = False

    # H_3: x is an element of G
    try:
        h3_ok = x in G
    except Exception:
        h3_ok = False

    # ¬Q: The cardinality of the double coset H x K is NOT equal to |H| |K| / |H \cap x K x^{-1}|
    try:
        if isinstance(H, PermutationGroup):
            H_set = set(H.elements)
        else:
            H_set = set(H)

        if isinstance(K, PermutationGroup):
            K_elements = list(K.elements)
        else:
            K_elements = list(K)

        HxK = set()
        for h in H_set:
            for k in K_elements:
                HxK.add(h * x * k)

        xKx_inv = set()
        x_inv = ~x
        for k in K_elements:
            xKx_inv.add(x * k * x_inv)

        intersection = H_set.intersection(xKx_inv)

        # We check len(HxK) != (|H| * |K|) / |intersection|
        # Rewritten to avoid division by zero and float comparison:
        neg_q_ok = len(HxK) * len(intersection) != len(H_set) * len(K_elements)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: K is a subgroup of G",
    "H_3: x is an element of G",
    "¬Q: |H x K| is not equal to |H| |K| / |H \\cap x K x^{-1}|"
]

N_HYP = 3
NEG_Q_INDEX = 3