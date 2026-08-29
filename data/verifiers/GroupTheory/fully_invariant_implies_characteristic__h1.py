import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.homomorphisms import homomorphism
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

# Top-level setup: named object bindings
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

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture:
    "If H is a fully invariant subgroup of G, then H is a characteristic subgroup of G."
    
    The witness should be a tuple (G, H) where G and H are PermutationGroup objects.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        elif hasattr(witness, 'G') and hasattr(witness, 'H'):
            G = witness.G
            H = witness.H
        else:
            return [False, False]
    except Exception:
        return [False, False]
    
    # H_1: H is a fully invariant subgroup of G
    try:
        if not hasattr(H, 'is_subgroup') or not H.is_subgroup(G):
            h1 = False
        else:
            gens = G.generators
            elements = list(G.generate())
            h1 = True
            # Check all endomorphisms
            for images in itertools.product(elements, repeat=len(gens)):
                try:
                    phi = homomorphism(G, G, gens, images)
                    if phi is not None:
                        for h in H.generators:
                            if phi(h) not in H:
                                h1 = False
                                break
                except Exception:
                    pass
                if not h1:
                    break
    except Exception:
        h1 = False

    # ¬Q: H is not a characteristic subgroup of G
    try:
        if not hasattr(H, 'is_subgroup') or not H.is_subgroup(G):
            q = False
        else:
            gens = G.generators
            elements = list(G.generate())
            q = True
            # Check all automorphisms
            for images in itertools.product(elements, repeat=len(gens)):
                try:
                    if len(images) == 0:
                        img_order = 1
                    else:
                        img_order = PermutationGroup(*images).order()
                    
                    # Since G is finite, an endomorphism is an automorphism iff it is surjective
                    if img_order == G.order():
                        phi = homomorphism(G, G, gens, images)
                        if phi is not None:
                            for h in H.generators:
                                if phi(h) not in H:
                                    q = False
                                    break
                except Exception:
                    pass
                if not q:
                    break
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a fully invariant subgroup of G",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1