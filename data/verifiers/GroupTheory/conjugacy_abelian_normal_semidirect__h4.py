import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        G, N, H, n1, n2 = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and n1 in G and n2 in G
    except Exception:
        h1 = False

    try:
        h2 = (isinstance(N, PermutationGroup) and 
              N.is_abelian and 
              all(n in G for n in N.generators) and 
              all(g * n * ~g in N for g in G.generators for n in N.generators))
    except Exception:
        h2 = False

    try:
        h3 = (isinstance(H, PermutationGroup) and 
              all(h in G for h in H.generators) and 
              not any(h in N for h in H.elements if not h.is_Identity) and 
              (N.order() * H.order() == G.order()))
    except Exception:
        h3 = False

    try:
        conj_G = any(g * n1 * ~g == n2 for g in G.elements)
        conj_H = any(h * n1 * ~h == n2 for h in H.elements)
        neg_q = (conj_G != conj_H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and n1, n2 are elements of G",
    "H_2: N is an abelian normal subgroup of G",
    "H_3: H is a subgroup of G such that G is the internal semidirect product of N and H",
    "¬Q: The equivalence (n1 and n2 are conjugate in G iff they are conjugate by an element of H) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3