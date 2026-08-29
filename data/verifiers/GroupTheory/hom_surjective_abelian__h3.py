import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = hasattr(G, "elements") and hasattr(H, "elements") and hasattr(H, "is_abelian")
    except Exception:
        h1 = False

    # H_2: phi is a surjective group homomorphism from G to H
    try:
        if not h1:
            h2 = False
        else:
            is_homo = True
            images = set()
            elements_G = list(G.elements)
            elements_H = set(H.elements)
            
            for x in elements_G:
                px = phi[x] if isinstance(phi, dict) else phi(x)
                images.add(px)
                if px not in elements_H:
                    is_homo = False
                    break
                    
            if is_homo:
                for x in elements_G:
                    for y in elements_G:
                        px = phi[x] if isinstance(phi, dict) else phi(x)
                        py = phi[y] if isinstance(phi, dict) else phi(y)
                        pxy = phi[x * y] if isinstance(phi, dict) else phi(x * y)
                        if pxy != px * py:
                            is_homo = False
                            break
                    if not is_homo:
                        break
                        
            is_surj = (images == elements_H)
            h2 = is_homo and is_surj
    except Exception:
        h2 = False

    # ¬Q: H is not an abelian group
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = not bool(H.is_abelian)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a surjective group homomorphism from G to H",
    "¬Q: H is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2