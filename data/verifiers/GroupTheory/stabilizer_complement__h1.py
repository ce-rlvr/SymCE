import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness can be a tuple (G, X, Y) or (G, X, Y, action).
    """
    # H1: X is a set on which G acts
    try:
        if len(witness) == 3:
            G, X, Y = witness
            action = lambda g, x: g(x)
        elif len(witness) == 4:
            G, X, Y, action = witness
        else:
            raise ValueError
            
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        if not isinstance(X, (set, list, tuple)):
            h1 = False
        else:
            # Verify action is callable and works on X
            if elements and X:
                _ = action(elements[0], list(X)[0])
            h1 = True
    except Exception:
        h1 = False

    # H2: Y is a subset of X
    try:
        if len(witness) == 3:
            _, X, Y = witness
        elif len(witness) == 4:
            _, X, Y, _ = witness
        else:
            raise ValueError
            
        h2 = set(Y).issubset(set(X))
    except Exception:
        h2 = False

    # neg_Q: The setwise stabilizer of Y in G is not equal to the setwise stabilizer of X \ Y in G
    try:
        if len(witness) == 3:
            G, X, Y = witness
            action = lambda g, x: g(x)
        elif len(witness) == 4:
            G, X, Y, action = witness
        else:
            raise ValueError
            
        X_set = set(X)
        Y_set = set(Y)
        X_minus_Y = X_set - Y_set
        
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        stab_Y_indices = set()
        stab_X_minus_Y_indices = set()
        
        for i, g in enumerate(elements):
            # Check if g stabilizes Y setwise
            g_Y = {action(g, y) for y in Y_set}
            if g_Y == Y_set:
                stab_Y_indices.add(i)
                
            # Check if g stabilizes X \ Y setwise
            g_X_minus_Y = {action(g, z) for z in X_minus_Y}
            if g_X_minus_Y == X_minus_Y:
                stab_X_minus_Y_indices.add(i)
                
        neg_q = (stab_Y_indices != stab_X_minus_Y_indices)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set on which G acts",
    "H_2: Y is a subset of X",
    "¬Q: The setwise stabilizer of Y in G is not equal to the setwise stabilizer of X \\setminus Y in G"
]

N_HYP = 2
NEG_Q_INDEX = 2