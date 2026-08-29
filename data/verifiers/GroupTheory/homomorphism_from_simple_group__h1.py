import sympy
from sympy.combinatorics import PermutationGroup
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

def conditions(witness):
    try:
        if hasattr(witness, 'domain') and hasattr(witness, 'codomain'):
            f = witness
            G = f.domain
            H = f.codomain
        else:
            G, H, f = witness
    except Exception:
        return [False, False, False]

    # H1: G is a simple group
    try:
        h1 = bool(G.is_simple)
    except Exception:
        h1 = False

    # H2: f is a group homomorphism from G to H
    try:
        if hasattr(f, 'domain') and hasattr(f, 'codomain'):
            h2 = (f.domain == G and f.codomain == H)
        elif isinstance(f, dict):
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            h2 = True
            for g in G_elements:
                if g not in f or f[g] not in H_elements:
                    h2 = False
                    break
            if h2:
                for g1 in G_elements:
                    for g2 in G_elements:
                        if f[g1 * g2] != f[g1] * f[g2]:
                            h2 = False
                            break
                    if not h2:
                        break
        elif callable(f):
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            h2 = True
            for g in G_elements:
                img = f(g)
                if img not in H_elements:
                    h2 = False
                    break
            if h2:
                for g1 in G_elements:
                    for g2 in G_elements:
                        if f(g1 * g2) != f(g1) * f(g2):
                            h2 = False
                            break
                    if not h2:
                        break
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: f is neither injective nor trivial
    try:
        if hasattr(f, 'is_injective'):
            inj = f.is_injective() if callable(f.is_injective) else f.is_injective
        elif hasattr(f, 'kernel'):
            ker = f.kernel() if callable(f.kernel) else f.kernel
            if hasattr(ker, 'order'):
                inj = (ker.order() == 1)
            else:
                inj = (len(ker) == 1)
        elif isinstance(f, dict):
            G_elements = list(G.elements)
            values = [f[g] for g in G_elements]
            inj = (len(set(values)) == len(values))
        elif callable(f):
            G_elements = list(G.elements)
            values = [f(g) for g in G_elements]
            inj = (len(set(values)) == len(values))
        else:
            inj = False
            
        if hasattr(f, 'is_trivial'):
            triv = f.is_trivial() if callable(f.is_trivial) else f.is_trivial
        elif hasattr(f, 'images'):
            H_elements = list(H.elements)
            id_H = next((h for h in H_elements if h * h == h), None)
            if isinstance(f.images, dict):
                triv = all(img == id_H for img in f.images.values())
            elif isinstance(f.images, list):
                triv = all(img == id_H for img in f.images)
            else:
                triv = False
        elif isinstance(f, dict):
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            id_H = next((h for h in H_elements if h * h == h), None)
            triv = all(f[g] == id_H for g in G_elements)
        elif callable(f):
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            id_H = next((h for h in H_elements if h * h == h), None)
            triv = all(f(g) == id_H for g in G_elements)
        else:
            triv = False
            
        neg_q = not (bool(inj) or bool(triv))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a simple group",
    "H_2: f is a group homomorphism from G to H",
    "¬Q: f is neither an injective homomorphism nor the trivial homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2