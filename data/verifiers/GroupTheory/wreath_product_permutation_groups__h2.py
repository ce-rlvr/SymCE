import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
    G = X = H = Y = None
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            Y = witness.get('Y')
            X = witness.get('X', None)
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                G, H, Y = witness
            elif len(witness) == 4:
                if isinstance(witness[1], (list, set, tuple)):
                    G, X, H, Y = witness
                else:
                    G, H, Y, _ = witness
            elif len(witness) >= 5:
                G, X, H, Y = witness[:4]
        else:
            G = getattr(witness, 'G', None)
            H = getattr(witness, 'H', None)
            Y = getattr(witness, 'Y', None)
            X = getattr(witness, 'X', None)
            
        if X is None and hasattr(G, 'degree'):
            X = list(range(G.degree))
    except Exception:
        pass

    # H1: G is a group acting faithfully on a set X
    h1 = False
    try:
        if isinstance(G, PermutationGroup) and isinstance(X, (list, set, tuple)):
            X_set = set(X)
            acts_on_X = True
            for g in G.generators:
                for x in X_set:
                    if g(x) not in X_set:
                        acts_on_X = False
                        break
                if not acts_on_X:
                    break
            if acts_on_X:
                stab = G
                for x in X_set:
                    stab = stab.stabilizer(x)
                if stab.order() == 1:
                    h1 = True
    except Exception:
        h1 = False

    # H2: W is the restricted wreath product of G by H
    # We verify that H is a valid group and Y is a valid set on which H acts.
    # The wreath product W is uniquely determined by G, H, and Y.
    h2 = False
    try:
        if isinstance(H, PermutationGroup) and isinstance(Y, (list, set, tuple)):
            Y_set = set(Y)
            acts_on_Y = True
            for h in H.generators:
                for y in Y_set:
                    if h(y) not in Y_set:
                        acts_on_Y = False
                        break
                if not acts_on_Y:
                    break
            if acts_on_Y:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: W does not have a faithful action on the Cartesian product X \times Y
    # The restricted wreath product W acts faithfully on X \times Y if and only if
    # H acts faithfully on Y. Thus, the conclusion fails iff H does NOT act faithfully on Y.
    neg_q = False
    try:
        if h2:
            stab = H
            for y in Y_set:
                stab = stab.stabilizer(y)
            if stab.order() > 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting faithfully on a set X",
    "H_2: W is the restricted wreath product of G by H",
    "¬Q: W does not have a faithful action on the Cartesian product X \\times Y"
]

N_HYP = 2
NEG_Q_INDEX = 2