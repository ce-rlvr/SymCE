import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
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
    """
    Checks whether the witness is a valid counterexample to the conjecture.
    The witness can be a tuple (G, g, h, x) or (G, action, g, h, x).
    """
    try:
        if len(witness) == 5:
            G, action, g, h, x = witness
            act = action
        elif len(witness) == 4:
            G, g, h, x = witness
            def act(a, y):
                try:
                    return a(y)
                except Exception:
                    return a * y
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group acting on a set X
    try:
        if hasattr(G, 'is_group'):
            h1 = bool(G.is_group)
        else:
            h1 = hasattr(G, '__contains__') or hasattr(G, 'contains')
        # Verify that the action is computable for the given elements
        _ = act(g, x)
        _ = act(h, x)
    except Exception:
        h1 = False

    # H_2: h is an element of the centralizer C_G(g)
    try:
        if hasattr(G, 'contains'):
            in_G = G.contains(h) and G.contains(g)
        else:
            in_G = (h in G) and (g in G)
        
        commutes = (h * g == g * h)
        try:
            commutes_bool = bool(commutes)
        except Exception:
            commutes_bool = (commutes == True)
            
        h2 = bool(in_G and commutes_bool)
    except Exception:
        h2 = False

    # H_3: x \in X is a fixed point of g
    try:
        eq = (act(g, x) == x)
        try:
            h3 = bool(eq)
        except Exception:
            h3 = (eq == True)
    except Exception:
        h3 = False

    # ¬Q: The element h \cdot x is NOT a fixed point of g
    try:
        hx = act(h, x)
        eq = (act(g, hx) == hx)
        try:
            neg_q = not bool(eq)
        except Exception:
            neg_q = not (eq == True)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: h is an element of the centralizer C_G(g)",
    "H_3: x is a fixed point of g",
    "¬Q: h \cdot x is not a fixed point of g"
]

N_HYP = 3
NEG_Q_INDEX = 3