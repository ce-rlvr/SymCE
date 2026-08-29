import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3), Permutation(0, 3)(1, 2))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x')
            y = witness.get('y')
        elif hasattr(witness, 'G') and hasattr(witness, 'x') and hasattr(witness, 'y'):
            G = witness.G
            x = witness.x
            y = witness.y
        else:
            G = witness[0]
            x = witness[1]
            y = witness[2]
            
        try:
            x = set(x)
        except TypeError:
            x = set([x])
            
        try:
            y = set(y)
        except TypeError:
            y = set([y])
    except Exception:
        return [False, False, False, False]

    # H1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            if not all(isinstance(i, int) and i >= 0 for i in x): h1 = False
            if not all(isinstance(i, int) and i >= 0 for i in y): h1 = False
    except Exception:
        h1 = False

    # H2: G_{x,y} is the setwise stabilizer of {x, y} under the induced action
    try:
        if not h1 or G.order() > 10000:
            h2 = False
            G_xy = None
            G_xy_elements = set()
        else:
            elements = list(G.generate())
            G_xy_elements = []
            for g in elements:
                gx = set(g(p) if p < g.size else p for p in x)
                gy = set(g(p) if p < g.size else p for p in y)
                if (gx == x and gy == y) or (gx == y and gy == x):
                    G_xy_elements.append(g)
            expected_G_xy = PermutationGroup(G_xy_elements) if G_xy_elements else PermutationGroup([Permutation()])
            
            if isinstance(witness, dict) and 'G_xy' in witness:
                G_xy = witness['G_xy']
                h2 = G_xy.is_subgroup(expected_G_xy) and expected_G_xy.is_subgroup(G_xy)
            elif hasattr(witness, 'G_xy'):
                G_xy = witness.G_xy
                h2 = G_xy.is_subgroup(expected_G_xy) and expected_G_xy.is_subgroup(G_xy)
            else:
                G_xy = expected_G_xy
                h2 = True
            G_xy_elements = set(G_xy_elements)
    except Exception:
        h2 = False

    # H3: G_x and G_y are the pointwise stabilizers of x and y in G
    try:
        if not h1:
            h3 = False
            G_x = None
            G_y = None
        else:
            expected_G_x = G
            for p in x:
                if p < expected_G_x.degree:
                    expected_G_x = expected_G_x.stabilizer(p)
            expected_G_y = G
            for p in y:
                if p < expected_G_y.degree:
                    expected_G_y = expected_G_y.stabilizer(p)
                    
            if isinstance(witness, dict) and 'G_x' in witness and 'G_y' in witness:
                G_x = witness['G_x']
                G_y = witness['G_y']
                h3_x = G_x.is_subgroup(expected_G_x) and expected_G_x.is_subgroup(G_x)
                h3_y = G_y.is_subgroup(expected_G_y) and expected_G_y.is_subgroup(G_y)
                h3 = h3_x and h3_y
            elif hasattr(witness, 'G_x') and hasattr(witness, 'G_y'):
                G_x = witness.G_x
                G_y = witness.G_y
                h3_x = G_x.is_subgroup(expected_G_x) and expected_G_x.is_subgroup(G_x)
                h3_y = G_y.is_subgroup(expected_G_y) and expected_G_y.is_subgroup(G_y)
                h3 = h3_x and h3_y
            else:
                G_x = expected_G_x
                G_y = expected_G_y
                h3 = True
    except Exception:
        h3 = False

    # Conclusion: G_x \cap G_y is a normal subgroup of G_{x,y}, and the index divides 2
    try:
        if not (h1 and h2 and h3):
            neg_Q = False
        else:
            G_x_elements = set(G_x.generate())
            G_y_elements = set(G_y.generate())
            intersection_elements = G_x_elements.intersection(G_y_elements)
            
            is_subgroup = all(g in G_xy_elements for g in intersection_elements)
            
            is_normal = True
            for h in intersection_elements:
                for g in G_xy_elements:
                    conj = g * h * (~g)
                    if conj not in intersection_elements:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
            order_G_xy = len(G_xy_elements)
            order_intersection = len(intersection_elements)
            
            if order_intersection == 0:
                index_divides_2 = False
            else:
                index = order_G_xy / order_intersection
                index_divides_2 = (order_G_xy % order_intersection == 0) and (index in [1, 2])
                
            Q = is_subgroup and is_normal and index_divides_2
            neg_Q = not Q
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: G_{x,y} is the setwise stabilizer of the subset {x, y} under the induced action",
    "H_3: G_x and G_y are the pointwise stabilizers of x and y in G",
    "¬Q: G_x \\cap G_y is not a normal subgroup of G_{x,y} or its index does not divide 2"
]

N_HYP = 3
NEG_Q_INDEX = 3