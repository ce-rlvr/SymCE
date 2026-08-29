import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        G, H, x = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and all(g in G for g in H.generators)
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = isinstance(x, int) and 0 <= x < G.degree
    except Exception:
        h3 = False

    # neg_Q: G != H G_x
    try:
        G_x = G.stabilizer(x)
        H_elements = list(H.generate())
        Gx_elements = list(G_x.generate())
        HGx_size = len(set(h * g for h in H_elements for g in Gx_elements))
        
        try:
            g_order = G.order()
        except Exception:
            try:
                g_order = G.order
            except Exception:
                g_order = len(list(G.generate()))
                
        neg_q = HGx_size != g_order
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: H is a subgroup of G",
    "H_3: x is an element of X",
    "¬Q: G cannot be factored as G = H G_x"
]

N_HYP = 3
NEG_Q_INDEX = 3