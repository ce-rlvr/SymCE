import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        G, H, phi, N_gens = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G and H are groups
    try:
        h1 = hasattr(G, 'generate') and hasattr(H, 'generate') and hasattr(G, 'identity') and hasattr(H, 'identity')
        if h1:
            G_elements = list(G.generate())
            H_elements = list(H.generate())
        else:
            G_elements = []
            H_elements = []
    except Exception:
        h1 = False

    # H2: phi is a group homomorphism from G to H
    try:
        if not h1:
            h2 = False
        else:
            if callable(phi):
                phi_func = phi
            elif isinstance(phi, dict):
                phi_func = lambda g: phi[g]
            else:
                phi_func = None
            
            if phi_func is None:
                h2 = False
            else:
                h2 = True
                for g in G_elements:
                    if phi_func(g) not in H_elements:
                        h2 = False
                        break
                if h2:
                    for g1 in G_elements:
                        for g2 in G_elements:
                            if phi_func(g1 * g2) != phi_func(g1) * phi_func(g2):
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False

    # H3: N is a normal subgroup of G
    try:
        if not h1:
            h3 = False
        else:
            if isinstance(N_gens, PermutationGroup):
                N = N_gens
            else:
                N = PermutationGroup(N_gens)
            N_elements = list(N.generate())
            h3 = True
            for n in N_elements:
                if n not in G_elements:
                    h3 = False
                    break
            if h3:
                for g in G_elements:
                    for n in N_elements:
                        if (g * n * ~g) not in N_elements:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # neg_Q: Conclusion fails (i.e., N is not a subset of ker(phi))
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            neg_q = False
            for n in N_elements:
                if phi_func(n) != H.identity:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a group homomorphism from G to H",
    "H_3: N is a normal subgroup of G",
    "¬Q: There does not exist a unique group homomorphism bar_phi: G/N -> H such that phi(g) = bar_phi(gN)"
]

N_HYP = 3
NEG_Q_INDEX = 3