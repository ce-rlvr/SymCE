import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        G, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        if isinstance(G, PermutationGroup):
            elements = list(G.elements)
            h1 = len(elements) > 0
        else:
            h1 = False
            elements = []
    except Exception:
        h1 = False
        elements = []

    # H_2: phi is surjective
    try:
        if not h1:
            h2 = False
        else:
            if isinstance(phi, dict):
                domain = set(phi.keys())
                image = set(phi.values())
                h2 = (domain == set(elements)) and (image == set(elements))
            elif isinstance(phi, list) and all(isinstance(item, tuple) and len(item) == 2 for item in phi):
                mapping = dict(phi)
                domain = set(mapping.keys())
                image = set(mapping.values())
                h2 = (domain == set(elements)) and (image == set(elements))
            elif callable(phi):
                image = set(phi(g) for g in elements)
                h2 = (image == set(elements))
            else:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: phi is not an automorphism of G
    try:
        if not h1:
            neg_q = False
        else:
            if isinstance(phi, dict):
                mapping = phi
            elif isinstance(phi, list) and all(isinstance(item, tuple) and len(item) == 2 for item in phi):
                mapping = dict(phi)
            elif callable(phi):
                mapping = {g: phi(g) for g in elements}
            else:
                mapping = {}
            
            domain = set(mapping.keys())
            image = set(mapping.values())
            is_bijective = (domain == set(elements)) and (image == set(elements))
            
            is_homomorphism = True
            if is_bijective:
                for g in elements:
                    for h in elements:
                        if mapping[g * h] != mapping[g] * mapping[h]:
                            is_homomorphism = False
                            break
                    if not is_homomorphism:
                        break
            else:
                is_homomorphism = False
                
            is_automorphism = is_bijective and is_homomorphism
            neg_q = not is_automorphism
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: phi is surjective",
    "¬Q: phi is not an automorphism of G"
]

N_HYP = 2
NEG_Q_INDEX = 2