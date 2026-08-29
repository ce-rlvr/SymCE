import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(G):
    return hasattr(G, 'elements') or hasattr(G, 'generate')

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    else:
        return []

def is_automorphism(G, alpha, elements):
    if not elements:
        return False
    
    try:
        if isinstance(alpha, dict):
            images = [alpha[g] for g in elements]
        else:
            images = [alpha(g) for g in elements]
    except Exception:
        return False
        
    # Check bijection
    for e in elements:
        if e not in images:
            return False
            
    # Check homomorphism
    for i, g in enumerate(elements):
        for j, h in enumerate(elements):
            try:
                gh = g * h
                idx_gh = elements.index(gh)
                if images[idx_gh] != images[i] * images[j]:
                    return False
            except Exception:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        G = witness[0]
        alpha = witness[1]
    except Exception:
        return [False, False]
        
    try:
        if not is_group(G):
            H1 = False
        else:
            elements = get_elements(G)
            H1 = is_automorphism(G, alpha, elements)
    except Exception:
        H1 = False
        
    try:
        if not is_group(G):
            neg_Q = True
        else:
            elements = get_elements(G)
            # The conclusion states there exists x in Hol(G) such that conjugation by x 
            # restricts exactly to alpha on G.
            # Since Hol(G) = G \rtimes Aut(G), the element x = (e, alpha) always exists 
            # and satisfies this condition IF AND ONLY IF alpha is an automorphism of G.
            # Therefore, the conclusion holds iff alpha is an automorphism.
            # neg_Q is True iff the conclusion FAILS.
            neg_Q = not is_automorphism(G, alpha, elements)
    except Exception:
        neg_Q = True
        
    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: alpha is an automorphism of G",
    "¬Q: There does not exist x in Hol(G) such that conjugation by x restricts to alpha on G"
]

N_HYP = 1
NEG_Q_INDEX = 1