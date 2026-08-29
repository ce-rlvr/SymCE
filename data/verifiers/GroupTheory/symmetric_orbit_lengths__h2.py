import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness):
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: x and y are elements of X
    try:
        h2 = isinstance(x, (int, sympy.Integer)) and isinstance(y, (int, sympy.Integer)) and 0 <= x < G.degree and 0 <= y < G.degree
    except Exception:
        h2 = False
        
    # H_3: G_x and G_y are the stabilizers of x and y in G, respectively
    try:
        if h1 and h2:
            Gx = G.stabilizer(x)
            Gy = G.stabilizer(y)
            h3 = isinstance(Gx, PermutationGroup) and isinstance(Gy, PermutationGroup)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: The cardinality of the orbit of y under G_x is not equal to the cardinality of the orbit of x under G_y
    try:
        if h1 and h2 and h3:
            orbit_y_Gx = Gx.orbit(y)
            orbit_x_Gy = Gy.orbit(x)
            neg_q = len(orbit_y_Gx) != len(orbit_x_Gy)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are elements of X",
    "H_3: G_x and G_y are the stabilizers of x and y in G, respectively",
    "¬Q: The cardinality of the orbit of y under G_x is not equal to the cardinality of the orbit of x under G_y"
]

N_HYP = 3
NEG_Q_INDEX = 3