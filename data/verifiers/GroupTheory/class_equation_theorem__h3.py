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

def conditions(witness) -> list[bool]:
    G = None
    Z = None
    R = None

    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                G, R = witness
            elif len(witness) == 3:
                G, Z, R = witness
            else:
                G = witness
                R = []
        else:
            G = witness
            R = []
    except Exception:
        pass

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: Z(G) is the center of G
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            h2_ok = (Z == G.center())
        else:
            h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: The order of G is not equal to the order of Z(G) plus the sum over all x in R of the index (G : C_G(x))
    try:
        Z_group = G.center()
        Z_order = Z_group.order()
        G_order = G.order()
        
        sum_index = 0
        for x in R:
            C_G_x = G.centralizer(x)
            index = G_order // C_G_x.order()
            sum_index += index
            
        neg_q = bool(G_order != Z_order + sum_index)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: Z(G) is the center of G",
    "¬Q: |G| != |Z(G)| + sum_{x in R} (G : C_G(x))"
]

N_HYP = 2
NEG_Q_INDEX = 2