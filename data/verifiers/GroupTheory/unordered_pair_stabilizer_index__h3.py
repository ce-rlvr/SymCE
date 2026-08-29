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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, x, y = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: x and y are distinct elements of X
    try:
        h2 = (x != y) and isinstance(x, (int, sympy.Integer)) and isinstance(y, (int, sympy.Integer)) and (0 <= x < G.degree) and (0 <= y < G.degree)
    except Exception:
        h2 = False
        
    # H3: G_x and G_y are the pointwise stabilizers of x and y in G
    try:
        h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: The intersection G_x cap G_y is NOT a normal subgroup of G_{x,y}, OR the index does NOT divide 2
    try:
        Gx = G.stabilizer(x)
        Gy = G.stabilizer(y)
        Gxy_int = Gx.intersect(Gy)
        
        swapper = None
        for g in G.generate():
            if g(x) == y and g(y) == x:
                swapper = g
                break
                
        if swapper is not None:
            gens = list(Gxy_int.generators) + [swapper]
            G_setwise = PermutationGroup(gens)
        else:
            G_setwise = Gxy_int
            
        is_normal = True
        for g in G_setwise.generators:
            for h in Gxy_int.generators:
                conj = g * h * (~g)
                if not Gxy_int.contains(conj):
                    is_normal = False
                    break
            if not is_normal:
                break
                
        index = G_setwise.order() // Gxy_int.order()
        divides_2 = (2 % index == 0)
        
        q_holds = is_normal and divides_2
        neg_q = not q_holds
        
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: x and y are distinct elements of X",
    "H_3: G_x and G_y are the pointwise stabilizers of x and y in G",
    "¬Q: The intersection G_x cap G_y is NOT a normal subgroup of G_{x,y}, OR the index of G_x cap G_y in G_{x,y} does NOT divide 2"
]

N_HYP = 3
NEG_Q_INDEX = 3