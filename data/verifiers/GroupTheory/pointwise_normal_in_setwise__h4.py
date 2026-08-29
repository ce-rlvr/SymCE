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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    G, X, Y, G_Y = None, None, None, None
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, Y = witness
            elif len(witness) == 3:
                G, X, Y = witness
            elif len(witness) >= 4:
                G, X, Y, G_Y = witness[:4]
    except Exception:
        pass

    # H1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1 and X is None:
            X = set(range(G.degree))
        if h1:
            h1 = h1 and isinstance(X, (set, list, tuple))
    except Exception:
        h1 = False

    # H2: Y is a subset of X
    try:
        h2 = set(Y).issubset(set(X))
    except Exception:
        h2 = False

    # H3: G_Y is the setwise stabilizer of Y in G
    try:
        if not h1:
            h3 = False
        elif G.order() > 5000:
            h3 = False
        else:
            Y_set = set(Y)
            expected_G_Y_elts = set()
            for g in G.elements:
                valid = True
                mapped = set()
                for y in Y_set:
                    if y < 0 or y >= G.degree:
                        valid = False
                        break
                    mapped.add(g(y))
                if valid and mapped == Y_set:
                    expected_G_Y_elts.add(g)
            
            if G_Y is None:
                if not expected_G_Y_elts:
                    expected_G_Y_elts.add(Permutation(G.degree - 1) if G.degree > 0 else Permutation())
                G_Y = PermutationGroup(list(expected_G_Y_elts))
                h3 = True
            else:
                h3 = set(G_Y.elements) == expected_G_Y_elts
    except Exception:
        h3 = False

    # neg_Q: The pointwise stabilizer G_{(Y)} is NOT a normal subgroup of the setwise stabilizer G_Y
    try:
        if not h1 or G.order() > 5000:
            neg_q = False
        else:
            Y_set = set(Y)
            G_pY_elts = set()
            for g in G.elements:
                valid = True
                for y in Y_set:
                    if y < 0 or y >= G.degree:
                        valid = False
                        break
                    if g(y) != y:
                        valid = False
                        break
                if valid:
                    G_pY_elts.add(g)
            
            if not G_pY_elts:
                G_pY_elts.add(Permutation(G.degree - 1) if G.degree > 0 else Permutation())
            G_pY = PermutationGroup(list(G_pY_elts))
            
            if G_Y is None:
                expected_G_Y_elts = set()
                for g in G.elements:
                    valid = True
                    mapped = set()
                    for y in Y_set:
                        if y < 0 or y >= G.degree:
                            valid = False
                            break
                        mapped.add(g(y))
                    if valid and mapped == Y_set:
                        expected_G_Y_elts.add(g)
                if not expected_G_Y_elts:
                    expected_G_Y_elts.add(Permutation(G.degree - 1) if G.degree > 0 else Permutation())
                G_Y = PermutationGroup(list(expected_G_Y_elts))
                
            is_normal = True
            for h in G_pY.generators:
                for k in G_Y.generators:
                    if not G_pY.contains(k * h * ~k):
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: Y is a subset of X",
    "H_3: G_Y is the setwise stabilizer of Y in G",
    "¬Q: The pointwise stabilizer G_{(Y)} is not a normal subgroup of the setwise stabilizer G_Y"
]

N_HYP = 3
NEG_Q_INDEX = 3