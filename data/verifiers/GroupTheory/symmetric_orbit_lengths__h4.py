import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) == 3:
            G, x, y = witness
            X = None
        elif len(witness) == 4:
            G, X, x, y = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        if isinstance(G, PermutationGroup):
            h1 = True
        else:
            h1 = hasattr(G, 'stabilizer') and hasattr(G, 'orbit')
    except Exception:
        h1 = False

    # H_2: X is a finite set on which G acts transitively
    try:
        if X is not None:
            if hasattr(X, 'is_finite'):
                is_finite = bool(X.is_finite)
            else:
                is_finite = hasattr(X, '__len__')
        else:
            is_finite = True

        if hasattr(G, 'is_transitive'):
            if callable(G.is_transitive):
                is_trans = bool(G.is_transitive())
            else:
                is_trans = bool(G.is_transitive)
        else:
            is_trans = False
            
        h2 = is_finite and is_trans
    except Exception:
        h2 = False

    # H_3: x and y are elements of X
    try:
        if X is not None:
            h3 = (x in X) and (y in X)
        elif hasattr(G, 'degree'):
            h3 = (0 <= int(x) < G.degree) and (0 <= int(y) < G.degree)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The cardinality of the orbit of y under G_x is not equal to the cardinality of the orbit of x under G_y
    try:
        Gx = G.stabilizer(x)
        Gy = G.stabilizer(y)
        orbit_y = Gx.orbit(y)
        orbit_x = Gy.orbit(x)
        
        if hasattr(orbit_y, '__len__'):
            len_y = len(orbit_y)
        elif hasattr(orbit_y, 'cardinality'):
            len_y = orbit_y.cardinality()
        else:
            len_y = len(list(orbit_y))
            
        if hasattr(orbit_x, '__len__'):
            len_x = len(orbit_x)
        elif hasattr(orbit_x, 'cardinality'):
            len_x = orbit_x.cardinality()
        else:
            len_x = len(list(orbit_x))
            
        neg_q = len_y != len_x
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a finite set on which G acts transitively",
    "H_3: x and y are elements of X",
    "¬Q: The cardinality of the orbit of y under G_x is not equal to the cardinality of the orbit of x under G_y"
]

N_HYP = 3
NEG_Q_INDEX = 3