import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G = witness['G']
        X = witness['X']
        action = witness['action']
        x = witness['x']
        H = witness['H']
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
            h1 = True
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    if not h1:
        return [False, False, False, False, False]

    try:
        if hasattr(H, 'generate'):
            H_elements = list(H.generate())
        elif hasattr(H, 'elements'):
            H_elements = list(H.elements)
        else:
            H_elements = list(H)
    except Exception:
        H_elements = []

    # H2: G acts transitively on X
    try:
        h2 = True
        for y in X:
            for z in X:
                if not any(action(g, y) == z for g in elements):
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # H3: x \in X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # H4: H = Stab(x)
    try:
        expected_H = set(g for g in elements if action(g, x) == x)
        h4 = set(H_elements) == expected_H
    except Exception:
        h4 = False

    # Conclusion: \phi is a G-set isomorphism
    try:
        phi_is_iso = True
        
        def coset(g, H_list):
            return frozenset(g * h for h in H_list)
            
        # 1. Well-defined
        for g1 in elements:
            for g2 in elements:
                if coset(g1, H_elements) == coset(g2, H_elements):
                    if action(g1, x) != action(g2, x):
                        phi_is_iso = False
                        
        # 2. Injective
        for g1 in elements:
            for g2 in elements:
                if action(g1, x) == action(g2, x):
                    if coset(g1, H_elements) != coset(g2, H_elements):
                        phi_is_iso = False
                        
        # 3. Surjective
        for y in X:
            if not any(action(g, x) == y for g in elements):
                phi_is_iso = False
                
        # 4. G-equivariant
        for g in elements:
            for a in elements:
                if action(g * a, x) != action(g, action(a, x)):
                    phi_is_iso = False
                    
        neg_q = not phi_is_iso
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts transitively on X",
    "H_3: x in X",
    "H_4: H = Stab(x)",
    "¬Q: phi is not a G-set isomorphism"
]

N_HYP = 4
NEG_Q_INDEX = 4