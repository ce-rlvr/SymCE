import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H, N, phi_input = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G and H are groups, phi maps G to H
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
        if h1:
            g_elems = list(G.elements)
            h_elems = list(H.elements)
            phi = {}
            if isinstance(phi_input, dict):
                for g in g_elems:
                    if g not in phi_input:
                        h1 = False
                        break
                    val = phi_input[g]
                    if val not in h_elems:
                        h1 = False
                        break
                    phi[g] = val
            elif callable(phi_input):
                for g in g_elems:
                    val = phi_input(g)
                    if val not in h_elems:
                        h1 = False
                        break
                    phi[g] = val
            else:
                h1 = False
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            h2 = bool(N.is_subgroup(G) and N.is_normal(G))
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: N is a subset of ker(phi)
    try:
        h3 = True
        if h1 and isinstance(N, PermutationGroup):
            h_id = H.identity
            for n in list(N.elements):
                if n not in phi:
                    h3 = False
                    break
                if phi[n] != h_id:
                    h3 = False
                    break
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: Conclusion fails.
    try:
        if h1:
            is_hom = True
            g_elems = list(G.elements)
            for g1 in g_elems:
                for g2 in g_elems:
                    if phi[g1 * g2] != phi[g1] * phi[g2]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            neg_q = not is_hom
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups and phi is a map from G to H",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a subset of ker(phi)",
    "¬Q: There does not exist a unique group homomorphism phi_bar: G/N -> H such that phi(g) = phi_bar(gN)"
]

N_HYP = 3
NEG_Q_INDEX = 3