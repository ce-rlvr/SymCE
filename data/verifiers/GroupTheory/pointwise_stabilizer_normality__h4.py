import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
trivial = PermutationGroup(Permutation(0))

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 2:
            G, Y = witness
            is_perm = True
        elif len(witness) == 4:
            G, X, action, Y = witness
            is_perm = False
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: G is a group acting on a set X
    try:
        if is_perm:
            h1 = isinstance(G, PermutationGroup)
        else:
            h1 = (isinstance(G, PermutationGroup) or hasattr(G, '__iter__')) and callable(action)
    except Exception:
        h1 = False

    # H2: Y is a subset of X
    try:
        if is_perm:
            h2 = isinstance(Y, (set, list, tuple)) and all(isinstance(y, (int, sympy.Integer)) for y in Y)
        else:
            h2 = isinstance(Y, (set, list, tuple)) and all(y in X for y in Y)
    except Exception:
        h2 = False

    # neg_Q: G_{(Y)} is NOT a normal subgroup of G_Y
    try:
        Y_set = set(Y)
        if is_perm:
            elements = list(G.generate())
            
            G_Y = []
            for g in elements:
                if {g(y) for y in Y_set} == Y_set:
                    G_Y.append(g)
                    
            G_pointwise = []
            for g in elements:
                if all(g(y) == y for y in Y_set):
                    G_pointwise.append(g)
                    
            is_normal = True
            for h in G_pointwise:
                for g in G_Y:
                    conj1 = g * h * ~g
                    conj2 = ~g * h * g
                    if not all(conj1(y) == y for y in Y_set):
                        is_normal = False
                        break
                    if not all(conj2(y) == y for y in Y_set):
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = not is_normal
        else:
            if isinstance(G, PermutationGroup):
                elements = list(G.generate())
            else:
                elements = list(G)
                
            G_Y = []
            for g in elements:
                mapped_Y = {action(g, y) for y in Y_set}
                if mapped_Y == Y_set:
                    G_Y.append(g)
            
            G_pointwise = []
            for g in elements:
                if all(action(g, y) == y for y in Y_set):
                    G_pointwise.append(g)
                    
            is_normal = True
            for g in G_Y:
                for h in G_pointwise:
                    try:
                        try:
                            g_inv = ~g
                        except Exception:
                            g_inv = g**-1
                        conj1 = g * h * g_inv
                        conj2 = g_inv * h * g
                        if not all(action(conj1, y) == y for y in Y_set):
                            is_normal = False
                            break
                        if not all(action(conj2, y) == y for y in Y_set):
                            is_normal = False
                            break
                    except Exception:
                        found_h_prime = False
                        for h_prime in G_pointwise:
                            if all(action(g, action(h, x)) == action(h_prime, action(g, x)) for x in X):
                                found_h_prime = True
                                break
                        if not found_h_prime:
                            is_normal = False
                            break
                if not is_normal:
                    break
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: Y is a subset of X",
    "¬Q: The pointwise stabilizer G_{(Y)} is not a normal subgroup of the setwise stabilizer G_{Y}"
]

N_HYP = 2
NEG_Q_INDEX = 2