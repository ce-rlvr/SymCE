import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(G):
    if hasattr(G, 'elements'):
        return set(G.elements)
    elif hasattr(G, 'generate'):
        return set(G.generate())
    elif isinstance(G, (list, set, tuple)):
        return set(G)
    return set()

def is_group(elements):
    if not elements: 
        return False
    elements = set(elements)
    
    identity = None
    for e in elements:
        if all(e * x == x and x * e == x for x in elements):
            identity = e
            break
    if identity is None:
        return False
        
    for x in elements:
        has_inv = False
        for y in elements:
            try:
                xy = x * y
            except Exception:
                return False
            if xy not in elements:
                return False
            if xy == identity and y * x == identity:
                has_inv = True
        if not has_inv:
            return False
            
    return True

def evaluate_phi(phi, x):
    if isinstance(phi, dict):
        return phi[x]
    else:
        return phi(x)

def conditions(witness) -> list[bool]:
    try:
        G, phi = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group and phi is a well-defined map on G
    try:
        elements = get_elements(G)
        if not elements:
            h1 = False
        elif not is_group(elements):
            h1 = False
        else:
            h1 = True
            for x in elements:
                try:
                    px = evaluate_phi(phi, x)
                    if px not in elements:
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: phi is an automorphism of G
    try:
        if not h1:
            h2 = False
        else:
            elements = get_elements(G)
            mapped = set()
            for x in elements:
                mapped.add(evaluate_phi(phi, x))
            if mapped != elements:
                h2 = False
            else:
                h2 = True
                for x in elements:
                    for y in elements:
                        if evaluate_phi(phi, x * y) != evaluate_phi(phi, x) * evaluate_phi(phi, y):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # ¬Q: phi(Z(G)) != Z(G)
    try:
        if not h1:
            neg_q = False
        else:
            elements = get_elements(G)
            center = set()
            for x in elements:
                if all(x * y == y * x for y in elements):
                    center.add(x)
            
            phi_center = {evaluate_phi(phi, x) for x in center}
            neg_q = (phi_center != center)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: phi is an automorphism of G",
    "¬Q: phi(Z(G)) is not equal to Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2