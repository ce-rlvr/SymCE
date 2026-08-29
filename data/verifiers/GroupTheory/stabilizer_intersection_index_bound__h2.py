import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    G, H, K = None, None, None
    
    try:
        if isinstance(witness, tuple) and len(witness) >= 3:
            G = witness[0]
            a = witness[-2]
            b = witness[-1]
            
            if hasattr(a, 'is_subgroup') or hasattr(a, 'elements'):
                H, K = a, b
            else:
                H = G.stabilizer(a)
                K = G.stabilizer(b)
    except Exception:
        pass

    # H1: G is a group acting on a set X
    try:
        h1 = hasattr(G, 'order') and hasattr(G, 'elements')
    except Exception:
        h1 = False

    # H2: The point stabilizers G_x and G_y have finite index in G
    try:
        if h1 and H is not None and K is not None:
            if hasattr(H, 'is_subgroup') and hasattr(K, 'is_subgroup'):
                h2 = H.is_subgroup(G) and K.is_subgroup(G)
            else:
                elements_G = set(G.elements)
                elements_H = set(H.elements)
                elements_K = set(K.elements)
                h2 = elements_H.issubset(elements_G) and elements_K.issubset(elements_G)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The index [G : G_x \cap G_y] is infinite or strictly greater than [G : G_x][G : G_y]
    try:
        if h1 and h2:
            order_G = G.order()
            order_H = H.order()
            order_K = K.order()
            
            index_H = order_G // order_H
            index_K = order_G // order_K
            
            try:
                if hasattr(H, 'intersection'):
                    H_cap_K = H.intersection(K)
                    order_cap = H_cap_K.order()
                elif hasattr(H, 'intersect'):
                    H_cap_K = H.intersect(K)
                    order_cap = H_cap_K.order()
                else:
                    raise AttributeError
            except Exception:
                elements_H = set(H.elements)
                elements_K = set(K.elements)
                elements_cap = elements_H.intersection(elements_K)
                order_cap = len(elements_cap)
            
            index_cap = order_G // order_cap
            
            neg_q = bool(index_cap > index_H * index_K)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: The point stabilizers G_x and G_y have finite index in G",
    "¬Q: The index of G_x cap G_y in G is infinite or strictly greater than the product of their indices"
]

N_HYP = 2
NEG_Q_INDEX = 2