import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(3), Permutation(0,1)(2,3), Permutation(0,2)(1,3), Permutation(0,3)(1,2))
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
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            Y = witness.get('Y')
            action_XY = witness.get('action_XY')
            action_X = witness.get('action_X')
            action_Y = witness.get('action_Y')
            x = witness.get('x')
            id_G = witness.get('id_G')
            mul = witness.get('mul')
        else:
            G = witness.G
            X = witness.X
            Y = witness.Y
            action_XY = witness.action_XY
            action_X = witness.action_X
            action_Y = witness.action_Y
            x = witness.x
            id_G = witness.id_G
            mul = witness.mul
            
        G_elements = list(G)
    except Exception:
        return [False] * 4 + [False]

    # H1: G is a group
    try:
        h1 = True
        if id_G not in G_elements:
            h1 = False
        else:
            for g in G_elements:
                if mul(g, id_G) != g or mul(id_G, g) != g:
                    h1 = False
                    break
                has_inv = False
                for h in G_elements:
                    if mul(g, h) == id_G and mul(h, g) == id_G:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
                for h in G_elements:
                    for k in G_elements:
                        if mul(mul(g, h), k) != mul(g, mul(h, k)):
                            h1 = False
                            break
                    if not h1: break
                if not h1: break
    except Exception:
        h1 = False

    # H2: X and Y are disjoint sets
    try:
        X_list = list(X)
        Y_list = list(Y)
        h2 = True
        for y_elem in Y_list:
            if y_elem in X_list:
                h2 = False
                break
    except Exception:
        h2 = False

    # H3: G acts on the disjoint union X \sqcup Y such that g \cdot z is defined by the action on X if z \in X, and by the action on Y if z \in Y
    try:
        XY_list = X_list + Y_list
        h3 = True
        for z in XY_list:
            if action_XY(id_G, z) != z:
                h3 = False
                break
            for g in G_elements:
                gz = action_XY(g, z)
                if gz not in XY_list:
                    h3 = False
                    break
                for h in G_elements:
                    if action_XY(mul(g, h), z) != action_XY(g, action_XY(h, z)):
                        h3 = False
                        break
                if not h3: break
            if not h3: break
        
        if h3:
            for g in G_elements:
                for z in X_list:
                    if action_XY(g, z) != action_X(g, z):
                        h3 = False
                        break
                for z in Y_list:
                    if action_XY(g, z) != action_Y(g, z):
                        h3 = False
                        break
                if not h3: break
    except Exception:
        h3 = False

    # H4: x is an element of X
    try:
        h4 = x in X_list
    except Exception:
        h4 = False

    # neg_Q: The conclusion fails
    try:
        stab_XY = set()
        for g in G_elements:
            if action_XY(g, x) == x:
                # We use string representation or id to handle unhashable elements if necessary,
                # but assuming elements are hashable or we can compare them directly.
                stab_XY.add(g)
                
        stab_X = set()
        for g in G_elements:
            if action_X(g, x) == x:
                stab_X.add(g)
                
        neg_q = (stab_XY != stab_X)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X and Y are disjoint sets",
    "H_3: G acts on X \\sqcup Y with action matching action on X and Y",
    "H_4: x is an element of X",
    "¬Q: The stabilizer of x in X \\sqcup Y is not equal to the stabilizer of x in X"
]

N_HYP = 4
NEG_Q_INDEX = 4