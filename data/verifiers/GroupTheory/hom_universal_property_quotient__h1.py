import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a subset of the kernel of phi",
    "¬Q: There does not exist a unique group homomorphism phi_bar: G/N -> H such that phi(g) = phi_bar(gN) for all g in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, H, phi, N = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        G_elements = list(G.elements)
        H_elements = list(H.elements)
        id_G = G.identity
        id_H = H.identity
        if hasattr(N, 'elements'):
            N_elements = list(N.elements)
        else:
            N_elements = list(N)
    except Exception:
        return [False, False, False, False]

    def get_phi(g):
        if isinstance(phi, dict):
            return phi[g]
        else:
            return phi(g)

    # H_1: phi is a group homomorphism from G to H
    try:
        h1 = True
        for g in G_elements:
            try:
                val = get_phi(g)
            except Exception:
                h1 = False
                break
            if val not in H_elements:
                h1 = False
                break
        if h1:
            for g1 in G_elements:
                for g2 in G_elements:
                    if get_phi(g1 * g2) != get_phi(g1) * get_phi(g2):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = True
        if not N_elements:
            h2 = False
        else:
            for n in N_elements:
                if n not in G_elements:
                    h2 = False
                    break
            if h2:
                if id_G not in N_elements:
                    h2 = False
                else:
                    for n1 in N_elements:
                        for n2 in N_elements:
                            if n1 * (n2**-1) not in N_elements:
                                h2 = False
                                break
                        if not h2:
                            break
            if h2:
                for g in G_elements:
                    for n in N_elements:
                        if g * n * (g**-1) not in N_elements:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H_3: N is a subset of the kernel of phi
    try:
        h3 = True
        for n in N_elements:
            if get_phi(n) != id_H:
                h3 = False
                break
    except Exception:
        h3 = False

    # ¬Q: There does not exist a unique group homomorphism phi_bar: G/N -> H such that phi(g) = phi_bar(gN)
    try:
        cosets = []
        for g in G_elements:
            coset = frozenset(g * n for n in N_elements)
            if coset not in cosets:
                cosets.append(coset)

        f = {}
        well_defined = True
        for C in cosets:
            vals = {get_phi(g) for g in C}
            if len(vals) != 1:
                well_defined = False
                break
            f[C] = list(vals)[0]

        if not well_defined:
            neg_q = True
        else:
            is_hom = True
            for C1 in cosets:
                for C2 in cosets:
                    g1 = next(iter(C1))
                    g2 = next(iter(C2))
                    C3 = frozenset(g1 * g2 * n for n in N_elements)
                    if f[C3] != f[C1] * f[C2]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            neg_q = not is_hom
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]