import sympy
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, phi = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a non-abelian group
    try:
        h1 = bool(not G.is_abelian)
    except Exception:
        h1 = False

    # H2: phi is an automorphism of G
    try:
        elements = list(G.elements)
        if callable(phi):
            phi_dict = {x: phi(x) for x in elements}
        else:
            phi_dict = phi
            
        if not isinstance(phi_dict, dict):
            h2 = False
        elif set(phi_dict.keys()) != set(elements) or set(phi_dict.values()) != set(elements):
            h2 = False
        else:
            h2 = True
            for x in elements:
                for y in elements:
                    if phi_dict[x * y] != phi_dict[x] * phi_dict[y]:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: For all x \in G \setminus Z(G), \phi(x) = x
    try:
        elements = list(G.elements)
        center = list(G.center().elements)
        if callable(phi):
            phi_dict = {x: phi(x) for x in elements}
        else:
            phi_dict = phi
            
        if not isinstance(phi_dict, dict):
            h3 = False
        else:
            h3 = True
            for x in elements:
                if x not in center:
                    if phi_dict[x] != x:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # neg_Q: phi is not the identity automorphism on G
    try:
        elements = list(G.elements)
        if callable(phi):
            phi_dict = {x: phi(x) for x in elements}
        else:
            phi_dict = phi
            
        if not isinstance(phi_dict, dict):
            neg_q = False
        else:
            neg_q = False
            for x in elements:
                if phi_dict[x] != x:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a non-abelian group",
    "H_2: phi is an automorphism of G",
    "H_3: For all x in G \\ Z(G), phi(x) = x",
    "¬Q: phi is not the identity automorphism on G"
]

N_HYP = 3
NEG_Q_INDEX = 3