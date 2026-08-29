import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f: G -> H is a surjective group homomorphism",
    "H_2: G is a finitely generated group",
    "¬Q: H is not a finitely generated group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    # Extract G, H, f if witness is a collection
    G = H = f = None
    if isinstance(witness, tuple) and len(witness) == 3:
        G, H, f = witness
    elif isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
        f = witness.get('f')
    else:
        G = getattr(witness, 'G', None)
        H = getattr(witness, 'H', None)
        f = getattr(witness, 'f', None)

    # Check H_1: f is a surjective group homomorphism
    try:
        if hasattr(witness, 'is_surjective_homomorphism'):
            val = witness.is_surjective_homomorphism
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'f_is_surjective') and hasattr(witness, 'f_is_homomorphism'):
            surj = witness.f_is_surjective
            hom = witness.f_is_homomorphism
            h1 = bool((surj() if callable(surj) else surj) and (hom() if callable(hom) else hom))
        elif f is not None:
            if hasattr(f, 'is_surjective') and hasattr(f, 'is_homomorphism'):
                surj = f.is_surjective
                hom = f.is_homomorphism
                h1 = bool((surj() if callable(surj) else surj) and (hom() if callable(hom) else hom))
            elif hasattr(f, 'is_surjective_homomorphism'):
                val = f.is_surjective_homomorphism
                h1 = bool(val() if callable(val) else val)
    except Exception:
        h1 = False

    # Check H_2: G is a finitely generated group
    try:
        if hasattr(witness, 'G_is_finitely_generated'):
            val = witness.G_is_finitely_generated
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_G_finitely_generated'):
            val = witness.is_G_finitely_generated
            h2 = bool(val() if callable(val) else val)
        elif G is not None:
            if hasattr(G, 'is_finitely_generated'):
                val = G.is_finitely_generated
                h2 = bool(val() if callable(val) else val)
            elif hasattr(G, 'generators'):
                h2 = len(list(G.generators)) < float('inf')
            elif isinstance(G, PermutationGroup):
                h2 = True
    except Exception:
        h2 = False

    # Check ¬Q: H is NOT a finitely generated group
    try:
        if hasattr(witness, 'H_is_finitely_generated'):
            val = witness.H_is_finitely_generated
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_H_finitely_generated'):
            val = witness.is_H_finitely_generated
            neg_q = not bool(val() if callable(val) else val)
        elif H is not None:
            if hasattr(H, 'is_finitely_generated'):
                val = H.is_finitely_generated
                neg_q = not bool(val() if callable(val) else val)
            elif hasattr(H, 'generators'):
                neg_q = len(list(H.generators)) == float('inf')
            elif isinstance(H, PermutationGroup):
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]