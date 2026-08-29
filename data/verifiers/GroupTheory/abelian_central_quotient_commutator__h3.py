import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
    # Support both witness = G and witness = (G, Z(G))
    if isinstance(witness, tuple) and len(witness) == 2:
        G, Z = witness
    else:
        G = witness
        Z = None

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: Z(G) is the center of G
    try:
        if Z is not None:
            if not h1_ok or not isinstance(Z, PermutationGroup):
                h2_ok = False
            else:
                Z_G = G.center()
                # Check if Z and Z_G are the same subgroup
                h2_ok = all(g in Z for g in Z_G.generators) and all(g in Z_G for g in Z.generators)
        else:
            # If Z is not explicitly provided, it is definitional
            h2_ok = h1_ok
    except Exception:
        h2_ok = False

    # ¬Q: The commutator subgroup G' is NOT a subgroup of the center Z(G)
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            G_prime = G.derived_subgroup()
            target_Z = Z if Z is not None else G.center()
            
            # Check if G' is a subgroup of Z(G)
            is_subgroup = all(g in target_Z for g in G_prime.generators)
            
            # We want the conclusion to FAIL
            neg_q_ok = not is_subgroup
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Z(G) is the center of G",
    "¬Q: The commutator subgroup G' is not a subgroup of the center Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2