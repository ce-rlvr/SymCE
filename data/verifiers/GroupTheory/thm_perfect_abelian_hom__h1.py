import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup,
    Permutation
)

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
    from sympy.combinatorics import homomorphism
    
    G_group = None
    H_group = None
    mapping = None
    phi = None

    # Parse the witness
    try:
        if type(witness).__name__ == 'Homomorphism':
            phi = witness
            G_group = phi.domain
            H_group = phi.codomain
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            G_group, H_group, mapping = witness
    except Exception:
        pass

    # H_1: H is an abelian group
    try:
        if H_group is not None:
            h1_ok = bool(H_group.is_abelian)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: phi is a group homomorphism from G to H
    try:
        if phi is not None:
            h2_ok = True
        elif G_group is not None and H_group is not None and mapping is not None:
            if callable(mapping):
                images = [mapping(g) for g in G_group.generators]
            else:
                images = mapping
            # homomorphism() raises ValueError if the mapping is not a valid homomorphism
            phi = homomorphism(G_group, H_group, images)
            h2_ok = True
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: phi is not the trivial homomorphism
    try:
        if phi is not None:
            is_trivial = True
            for g in G_group.generators:
                img = phi(g)
                img_is_id = False
                
                # Check various ways the identity element might be represented
                if hasattr(img, 'is_Identity') and img.is_Identity:
                    img_is_id = True
                elif hasattr(img, 'is_identity') and img.is_identity:
                    img_is_id = True
                elif hasattr(H_group, 'identity') and img == H_group.identity:
                    img_is_id = True
                
                if not img_is_id:
                    is_trivial = False
                    break
            neg_q_ok = not is_trivial
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is an abelian group",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: phi is not the trivial homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2