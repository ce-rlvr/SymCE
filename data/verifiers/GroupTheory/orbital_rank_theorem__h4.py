import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

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
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                G, X, x, G_x = witness
            elif len(witness) == 3:
                G, X, x = witness
                G_x = G.stabilizer(x)
            else:
                return [False, False, False, False]
        else:
            G = witness
            X = list(range(G.degree))
            x = 0
            G_x = G.stabilizer(x)
    except Exception:
        return [False, False, False, False]

    # H1: G is a group acting transitively on a set X
    try:
        X_set = set(X)
        if not X_set or not hasattr(G, 'generators'):
            h1 = False
        else:
            invariant = True
            for g in G.generators:
                for y in X_set:
                    if g(y) not in X_set:
                        invariant = False
                        break
                if not invariant:
                    break
            if not invariant:
                h1 = False
            else:
                x0 = list(X_set)[0]
                orb = {x0}
                queue = [x0]
                for curr in queue:
                    for g in G.generators:
                        nxt = g(curr)
                        if nxt not in orb:
                            orb.add(nxt)
                            queue.append(nxt)
                h1 = (orb == X_set)
    except Exception:
        h1 = False

    # H2: x is an element of X
    try:
        h2 = x in X_set
    except Exception:
        h2 = False

    # H3: G_x is the stabilizer of x in G
    try:
        if not hasattr(G, 'stabilizer') or not hasattr(G_x, 'generators'):
            h3 = False
        else:
            expected_G_x = G.stabilizer(x)
            h3 = True
            for g in G_x.generators:
                if g not in expected_G_x:
                    h3 = False
                    break
            if h3:
                for g in expected_G_x.generators:
                    if g not in G_x:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # Conclusion: The number of orbits of the restricted action of G_x on X 
    # is equal to the number of orbits of G acting on X \times X.
    try:
        unvisited_X = set(X_set)
        orbits_Gx = 0
        gens_Gx = G_x.generators
        if not gens_Gx:
            orbits_Gx = len(X_set)
        else:
            while unvisited_X:
                elem = unvisited_X.pop()
                orb = {elem}
                queue = [elem]
                for curr in queue:
                    for g in gens_Gx:
                        nxt = g(curr)
                        if nxt not in orb:
                            orb.add(nxt)
                            queue.append(nxt)
                unvisited_X -= orb
                orbits_Gx += 1

        unvisited_pairs = set(itertools.product(X_set, X_set))
        orbits_G_pairs = 0
        gens_G = G.generators
        if not gens_G:
            orbits_G_pairs = len(unvisited_pairs)
        else:
            while unvisited_pairs:
                elem = unvisited_pairs.pop()
                orb = {elem}
                queue = [elem]
                for curr in queue:
                    for g in gens_G:
                        nxt = (g(curr[0]), g(curr[1]))
                        if nxt not in orb:
                            orb.add(nxt)
                            queue.append(nxt)
                unvisited_pairs -= orb
                orbits_G_pairs += 1

        q = (orbits_Gx == orbits_G_pairs)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting transitively on a set X",
    "H_2: x is an element of X",
    "H_3: G_x is the stabilizer of x in G",
    "¬Q: The number of orbits of G_x on X is not equal to the number of orbits of G on X x X"
]

N_HYP = 3
NEG_Q_INDEX = 3