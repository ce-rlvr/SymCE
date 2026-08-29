import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False]
        G, H, N, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups (and phi is a well-defined map from G to H)
    try:
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            G_elems = list(G.generate())
            H_elems = set(H.generate())
            if callable(phi):
                h1 = all(phi(g) in H_elems for g in G_elems)
            elif isinstance(phi, dict):
                h1 = set(phi.keys()) == set(G_elems) and all(v in H_elems for v in phi.values())
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of H
    try:
        if isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup):
            N_elems = set(N.generate())
            H_elems = set(H.generate())
            if not N_elems.issubset(H_elems):
                h2 = False
            else:
                is_normal = True
                for n in N.generators:
                    for h in H.generators:
                        if (h * n * ~h) not in N_elems:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h2 = is_normal
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The preimage phi^-1(N) is NOT a normal subgroup of G
    try:
        N_elems = set(N.generate())
        if callable(phi):
            preimage = [g for g in G.generate() if phi(g) in N_elems]
        else:
            preimage = [g for g in G.generate() if phi[g] in N_elems]
        
        is_subgroup = True
        if not preimage:
            is_subgroup = False
        else:
            preimage_set = set(preimage)
            if G.identity not in preimage_set:
                is_subgroup = False
            else:
                # Check closure
                for a in preimage:
                    for b in preimage:
                        if (a * b) not in preimage_set:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                # Check inverses
                if is_subgroup:
                    for a in preimage:
                        if ~a not in preimage_set:
                            is_subgroup = False
                            break
        
        if not is_subgroup:
            neg_q = True
        else:
            # Check normality
            is_normal = True
            preimage_set = set(preimage)
            for n in preimage:
                for g in G.generate():
                    if (g * n * ~g) not in preimage_set:
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: N is a normal subgroup of H",
    "¬Q: The preimage phi^-1(N) is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2