import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
        G, X, Y = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: X is a set on which G acts
    try:
        if not isinstance(X, (set, list, tuple)):
            h2 = False
            X_set = set()
        else:
            X_set = set(X)
            if not all(isinstance(x, int) and x >= 0 for x in X_set):
                h2 = False
            else:
                h2 = True
                for g in G.generators:
                    if {g(x) for x in X_set} != X_set:
                        h2 = False
                        break
    except Exception:
        h2 = False
        X_set = set()
        
    # neg_Q: The setwise stabilizer of Y in G is NOT equal to the setwise stabilizer of X \ Y in G
    try:
        if not isinstance(Y, (set, list, tuple)):
            neg_q = False
        else:
            Y_set = set(Y)
            if not all(isinstance(y, int) and y >= 0 for y in Y_set):
                neg_q = False
            else:
                X_minus_Y = X_set - Y_set
                
                # Limit group size to ensure fast execution
                if getattr(G, 'order', lambda: 10001)() > 10000:
                    neg_q = False
                else:
                    stab_Y = set()
                    stab_X_minus_Y = set()
                    
                    for g in G.generate():
                        if {g(y) for y in Y_set} == Y_set:
                            stab_Y.add(g)
                        if {g(z) for z in X_minus_Y} == X_minus_Y:
                            stab_X_minus_Y.add(g)
                            
                    neg_q = (stab_Y != stab_X_minus_Y)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set on which G acts",
    "¬Q: The setwise stabilizer of Y in G is not equal to the setwise stabilizer of X \\ Y in G"
]

N_HYP = 2
NEG_Q_INDEX = 2