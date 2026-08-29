import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Standard group bindings
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, H, f) or (G, H, Z_G, f) where:
      - G and H are PermutationGroup objects
      - f is a homomorphism from G to H (callable, dict, or list of pairs)
    """
    try:
        if len(witness) == 3:
            G, H, f = witness
            Z_G_witness = None
        elif len(witness) == 4:
            G, H, Z_G_witness, f = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: Z(G) is the center of G and f is a homomorphism
    try:
        if h1:
            elements_G = list(G.generate())
            elements_H = list(H.generate())
            
            if callable(f):
                f_dict = {g: f(g) for g in elements_G}
            elif isinstance(f, dict):
                f_dict = f
            else:
                try:
                    f_dict = dict(f)
                except Exception:
                    f_dict = {}
                    
            maps_to_H = all(g in f_dict and f_dict[g] in elements_H for g in elements_G)
            
            is_hom = True
            if maps_to_H:
                for a in elements_G:
                    for b in elements_G:
                        if f_dict[a * b] != f_dict[a] * f_dict[b]:
                            is_hom = False
                            break
                    if not is_hom:
                        break
            else:
                is_hom = False
                
            center_G = set()
            for g in elements_G:
                if all(g * x == x * g for x in elements_G):
                    center_G.add(g)
                    
            h2 = is_hom and maps_to_H
            if Z_G_witness is not None:
                h2 = h2 and (set(Z_G_witness) == center_G)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The image f(Z(G)) is not a subgroup of the center of H
    try:
        if h1 and h2:
            center_H = set()
            for h in elements_H:
                if all(h * x == x * h for x in elements_H):
                    center_H.add(h)
            
            # Since f is a homomorphism, f(Z(G)) is a subgroup of H.
            # It is a subgroup of Z(H) iff it is a subset of Z(H).
            # The negation is that there is some element in f(Z(G)) not in Z(H).
            neg_q = any(f_dict[g] not in center_H for g in center_G)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: Z(G) is the center of G and f is a homomorphism",
    "¬Q: The image f(Z(G)) is not a subgroup of the center of H"
]

N_HYP = 2
NEG_Q_INDEX = 2