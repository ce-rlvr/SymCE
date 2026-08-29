import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness):
    # H1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H2: Hol(G) is the semidirect product G \rtimes Aut(G), where Aut(G) acts on G by evaluation
    # This is a definitional property of the construction.
    h2 = True

    # H3: N = {(g, id) | g \in G} is the canonical embedding of G into Hol(G)
    # This is a definitional property of the construction.
    h3 = True

    # neg_Q: N is NOT a normal subgroup of Hol(G)
    # N is normal in Hol(G) iff for all (g, a) in Hol(G) and (n, id) in N,
    # the conjugate (g, a)(n, id)(g, a)^-1 is in N.
    # The conjugate evaluates to (g * a(n) * g^-1, id).
    # This is in N iff g * a(n) * g^-1 is in G.
    # Since a(n) is an element of G, this is equivalent to checking if
    # g * m * g^-1 is in G for all g, m in G.
    try:
        if not h1:
            neg_q = False
        else:
            elements = list(witness.generate())
            elements_set = set(elements)
            is_normal = True
            for g in elements:
                g_inv = ~g
                for m in elements:
                    conj = g * m * g_inv
                    if conj not in elements_set:
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Hol(G) is the semidirect product G \\rtimes Aut(G)",
    "H_3: N is the canonical embedding of G into Hol(G)",
    "¬Q: N is not a normal subgroup of Hol(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3