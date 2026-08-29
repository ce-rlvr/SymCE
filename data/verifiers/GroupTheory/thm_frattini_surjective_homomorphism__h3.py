import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.homomorphisms import homomorphism

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: phi is a surjective group homomorphism
    try:
        if isinstance(phi, dict):
            if all(g in phi for g in G.elements):
                phi_eval = lambda x: phi[x]
            else:
                phi_hom = homomorphism(G, H, phi)
                phi_eval = lambda x: phi_hom(x)
        elif callable(phi):
            phi_eval = phi
        else:
            phi_eval = lambda x: phi(x)

        is_homo = True
        images = set()
        for g1 in G.elements:
            for g2 in G.elements:
                if phi_eval(g1) * phi_eval(g2) != phi_eval(g1 * g2):
                    is_homo = False
                    break
            if not is_homo:
                break

        if is_homo:
            for g in G.elements:
                images.add(phi_eval(g))
            h2 = is_homo and images == set(H.elements)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The image of the Frattini subgroup of G under phi is NOT contained in the Frattini subgroup of H
    try:
        def get_maximal_subgroups(group):
            try:
                return group.maximal_subgroups()
            except AttributeError:
                all_subs = group.subgroups()
                proper_subs = [s for s in all_subs if s.order() < group.order()]
                max_subs = []
                for s in proper_subs:
                    is_max = True
                    for other in proper_subs:
                        if s.order() < other.order() and set(s.elements).issubset(set(other.elements)):
                            is_max = False
                            break
                    if is_max:
                        max_subs.append(s)
                return max_subs

        # Compute Frattini subgroup of G
        max_subs_G = get_maximal_subgroups(G)
        if not max_subs_G:
            frat_G_elems = set(G.elements)
        else:
            frat_G_elems = set(max_subs_G[0].elements)
            for sub in max_subs_G[1:]:
                frat_G_elems = frat_G_elems.intersection(set(sub.elements))

        # Compute Frattini subgroup of H
        max_subs_H = get_maximal_subgroups(H)
        if not max_subs_H:
            frat_H_elems = set(H.elements)
        else:
            frat_H_elems = set(max_subs_H[0].elements)
            for sub in max_subs_H[1:]:
                frat_H_elems = frat_H_elems.intersection(set(sub.elements))

        # Compute image of Frattini subgroup of G under phi
        img_frat_G = set()
        for g in frat_G_elems:
            img_frat_G.add(phi_eval(g))

        # Check if it fails to be contained in the Frattini subgroup of H
        neg_q = not img_frat_G.issubset(frat_H_elems)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a surjective group homomorphism",
    "¬Q: phi(Phi(G)) is not contained in Phi(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2