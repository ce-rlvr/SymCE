import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
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
    """
    Checks the hypotheses and negated conclusion for the false conjecture.
    The witness is expected to be a tuple: (G, X, Y)
    where G is a PermutationGroup, and X and Y are iterables of integers.
    """
    # H_1: G is a group
    try:
        G, X, Y = witness
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: Y is a subset of X
    try:
        G, X, Y = witness
        h2_ok = set(Y).issubset(set(X))
    except Exception:
        h2_ok = False

    # ¬Q: The setwise stabilizer of Y in G is not equal to the setwise stabilizer of X \setminus Y in G
    try:
        G, X, Y = witness
        X_set = set(X)
        Y_set = set(Y)
        X_minus_Y = X_set - Y_set
        
        stab_Y = set()
        stab_X_minus_Y = set()
        
        for g in G.elements:
            # Check if g stabilizes Y setwise
            img_Y = set(g(y) for y in Y_set)
            if img_Y == Y_set:
                stab_Y.add(g)
                
            # Check if g stabilizes X \setminus Y setwise
            img_X_minus_Y = set(g(z) for z in X_minus_Y)
            if img_X_minus_Y == X_minus_Y:
                stab_X_minus_Y.add(g)
                
        neg_q_ok = (stab_Y != stab_X_minus_Y)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Y is a subset of X",
    "¬Q: The setwise stabilizer of Y in G is not equal to the setwise stabilizer of X \\setminus Y in G"
]

N_HYP = 2
NEG_Q_INDEX = 2