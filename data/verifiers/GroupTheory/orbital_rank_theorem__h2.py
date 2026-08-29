import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, X, x = witness
            elif len(witness) == 2:
                G, x = witness
                X = set(range(G.degree)) if hasattr(G, 'degree') else set()
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
    
    h1, h2, h3, neg_q = False, False, False, False

    # H_1: G is a group acting transitively on a set X
    try:
        if isinstance(G, PermutationGroup):
            X_set = set(X)
            if not all(isinstance(i, (int, sympy.Integer)) and i >= 0 for i in X_set):
                pass
            elif len(X_set) > 0:
                x0 = next(iter(X_set))
                orbit = set()
                queue = [x0]
                orbit.add(x0)
                while queue:
                    curr = queue.pop(0)
                    for g in G.generators:
                        nxt = g(curr)
                        if nxt not in orbit:
                            orbit.add(nxt)
                            queue.append(nxt)
                if orbit == X_set:
                    is_invariant = True
                    for g in G.generators:
                        for i in X_set:
                            if g(i) not in X_set:
                                is_invariant = False
                                break
                        if not is_invariant:
                            break
                    if is_invariant:
                        h1 = True
            elif len(X_set) == 0:
                h1 = True
    except Exception:
        pass

    # H_2: G_x is the stabilizer of x in G
    try:
        if isinstance(x, (int, sympy.Integer)):
            if x >= G.degree or x < 0:
                Gx = G
            else:
                Gx = G.stabilizer(x)
            h2 = True
    except Exception:
        pass

    # H_3: G acts on the Cartesian product X x X via the diagonal action
    try:
        if h1 and h2:
            h3 = True
    except Exception:
        pass

    # ¬Q: The number of orbits of G_x on X is not equal to the number of orbits of G on X x X
    try:
        if h1 and h2 and h3:
            # Calculate orbits of G_x on X
            orbits_Gx = set()
            for item in X_set:
                orbit = set()
                queue = [item]
                orbit.add(item)
                while queue:
                    curr = queue.pop(0)
                    for g in Gx.generators:
                        nxt = g(curr)
                        if nxt not in orbit:
                            orbit.add(nxt)
                            queue.append(nxt)
                orbits_Gx.add(frozenset(orbit))
            num_orbits_Gx = len(orbits_Gx)

            # Calculate orbits of G on X x X
            X_times_X = [(u, v) for u in X_set for v in X_set]
            orbits_G_XX = set()
            for pair in X_times_X:
                orbit = set()
                queue = [pair]
                orbit.add(pair)
                while queue:
                    curr = queue.pop(0)
                    for g in G.generators:
                        nxt = (g(curr[0]), g(curr[1]))
                        if nxt not in orbit:
                            orbit.add(nxt)
                            queue.append(nxt)
                orbits_G_XX.add(frozenset(orbit))
            num_orbits_G_XX = len(orbits_G_XX)

            if num_orbits_Gx != num_orbits_G_XX:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting transitively on a set X",
    "H_2: G_x is the stabilizer of x in G",
    "H_3: G acts on the Cartesian product X x X via the diagonal action",
    "¬Q: The number of orbits of G_x on X is not equal to the number of orbits of G on X x X"
]

N_HYP = 3
NEG_Q_INDEX = 3