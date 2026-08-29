import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            H = witness.get('H')
            n1 = witness.get('n1')
            h1 = witness.get('h1')
            n2 = witness.get('n2')
            h2 = witness.get('h2')
        else:
            G, N, H, n1, h1, n2, h2 = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is the internal semidirect product of normal subgroup N and subgroup H
    try:
        h1_ok = False
        if N.is_subgroup(G) and H.is_subgroup(G) and N.is_normal(G):
            # For internal semidirect product, we need N intersect H = {e} and NH = G.
            # Since N is normal, NH is a subgroup. |NH| = |N||H| / |N \cap H|.
            # If |N||H| == |G| and N \cap H = {e}, then NH = G.
            if N.order() * H.order() == G.order():
                trivial_int = True
                for h in H.elements:
                    if not h.is_Identity and h in N:
                        trivial_int = False
                        break
                h1_ok = trivial_int
    except Exception:
        h1_ok = False

    # H2: h1 and h2 are elements of H
    try:
        h2_ok = bool(h1 in H and h2 in H)
    except Exception:
        h2_ok = False

    # H3: n1 and n2 are elements of G (implicit from "elements n1 h1 and n2 h2 in G")
    try:
        h3_ok = bool(n1 in G and n2 in G)
    except Exception:
        h3_ok = False

    # ¬Q: The conclusion states that n1 * (h1 * n2 * h1^-1) is in N.
    # The conclusion fails if this element is NOT in N.
    try:
        part1 = n1 * h1 * n2 * h1**-1
        neg_q = bool(part1 not in N)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is the internal semidirect product of normal subgroup N and subgroup H",
    "H_2: h1 and h2 are elements of H",
    "H_3: n1 and n2 are elements of G",
    "¬Q: n1 * (h1 * n2 * h1^-1) is not in N"
]

N_HYP = 3
NEG_Q_INDEX = 3