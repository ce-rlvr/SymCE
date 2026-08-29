import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness):
    try:
        G, X, x = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a transitive permutation group acting on a set X
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            is_trans = G.is_transitive
            if callable(is_trans):
                is_trans = is_trans()
            
            if not is_trans:
                h1 = False
            else:
                acts = True
                for y in X:
                    if not isinstance(y, int) or y < 0:
                        acts = False
                        break
                if acts:
                    for g in G.generators:
                        for y in X:
                            if g(y) not in X:
                                acts = False
                                break
                        if not acts:
                            break
                h1 = acts
    except Exception:
        h1 = False

    # H2: X contains at least two elements
    try:
        h2 = len(X) >= 2
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # Conclusion: The action of G on X is primitive if and only if G_x is a maximal subgroup of G.
    try:
        def is_primitive_on(Grp, Y):
            Y_list = list(Y)
            if len(Y_list) < 2:
                return False
            
            orbit = set(Grp.orbit(Y_list[0]))
            if orbit != set(Y_list):
                return False
            
            mapping = {y: i for i, y in enumerate(Y_list)}
            new_gens = []
            for g in Grp.generators:
                new_perm = [mapping[g(y)] for y in Y_list]
                new_gens.append(Permutation(new_perm))
            
            H = PermutationGroup(new_gens)
            is_prim = H.is_primitive
            if callable(is_prim):
                return is_prim()
            return is_prim

        # Check if the action of G on X is primitive
        prim_on_X = is_primitive_on(G, X)

        # Check if G_x is a maximal subgroup of G
        # By the orbit-stabilizer theorem, G_x is maximal in G iff G acts primitively on the orbit of x
        orbit_x = set(G.orbit(x))
        if len(orbit_x) < 2:
            G_x_maximal = False
        else:
            G_x_maximal = is_primitive_on(G, orbit_x)

        conclusion = (prim_on_X == G_x_maximal)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a transitive permutation group acting on a set X",
    "H_2: X contains at least two elements",
    "H_3: x is an element of X",
    "¬Q: The action of G on X is primitive if and only if G_x is a maximal subgroup of G (fails)"
]

N_HYP = 3
NEG_Q_INDEX = 3