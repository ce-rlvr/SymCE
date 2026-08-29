import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    G, X, x, y, G_xy = None, None, None, None, None
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            x = witness.get('x')
            y = witness.get('y')
            G_xy = witness.get('G_xy')
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                G, x, y = witness
            elif len(witness) == 4:
                G, X, x, y = witness
            elif len(witness) == 5:
                G, X, x, y, G_xy = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup)
        if X is None and h1:
            X = set(range(G.degree))
        elif X is not None:
            h1 = h1 and isinstance(X, (set, list, tuple))
    except Exception:
        h1 = False

    # H_2: x and y are distinct elements of X
    try:
        h2 = (x != y) and (x in X) and (y in X)
        if h1:
            # Verify x and y are valid points for the permutation group
            _ = G.identity(x)
            _ = G.identity(y)
    except Exception:
        h2 = False

    # H_3: G_{x,y} is the setwise stabilizer of the subset {x, y}
    G_x_y = None
    try:
        if not (h1 and h2):
            raise ValueError
            
        G_x = G.stabilizer(x)
        G_x_y = G_x.stabilizer(y)
        
        swap_g = None
        for g in G.elements:
            if g(x) == y and g(y) == x:
                swap_g = g
                break
        
        if swap_g:
            computed_G_xy = PermutationGroup(G_x_y.generators + [swap_g])
        else:
            computed_G_xy = G_x_y
            
        if G_xy is not None:
            if isinstance(G_xy, PermutationGroup):
                h3 = computed_G_xy.is_subgroup(G_xy) and G_xy.is_subgroup(computed_G_xy)
            else:
                h3 = False
        else:
            G_xy = computed_G_xy
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: The intersection G_x \cap G_y is not a normal subgroup of G_{x,y}, 
    # or the index [G_{x,y} : G_x \cap G_y] does not divide 2
    try:
        if not (h1 and h2 and h3 and G_x_y is not None):
            raise ValueError
            
        is_normal = True
        for g in G_xy.generators:
            g_inv = ~g
            for h in G_x_y.generators:
                conj = g * h * g_inv
                if conj not in G_x_y:
                    is_normal = False
                    break
            if not is_normal:
                break
        
        order_G_xy = G_xy.order()
        order_G_x_y = G_x_y.order()
        
        if order_G_xy % order_G_x_y != 0:
            index_divides_2 = False
        else:
            index = order_G_xy // order_G_x_y
            index_divides_2 = (2 % index == 0)
            
        neg_Q = not (is_normal and index_divides_2)
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: x and y are distinct elements of X",
    "H_3: G_{x,y} is the setwise stabilizer of the subset {x, y} under the induced action of G on the power set of X",
    "not Q: The intersection G_x and G_y is not a normal subgroup of G_{x,y}, or the index does not divide 2"
]

N_HYP = 3
NEG_Q_INDEX = 3