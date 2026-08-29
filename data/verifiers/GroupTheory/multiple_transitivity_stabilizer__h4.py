import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if len(witness) == 4:
            G, X, k, x = witness
            X = set(X)
        elif len(witness) == 3:
            G, k, x = witness
            X = set(range(G.degree))
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(X, set)
        if h1:
            h1 = all(isinstance(e, (int, sympy.Integer)) for e in X)
    except Exception:
        h1 = False

    # H_2: k is an integer such that k >= 2
    try:
        h2 = isinstance(k, (int, sympy.Integer)) and k >= 2
    except Exception:
        h2 = False

    # H_3: X contains at least k elements
    try:
        h3 = len(X) >= k
    except Exception:
        h3 = False

    # neg_Q: The equivalence between G acting k-transitively and (G acting transitively and G_x acting (k-1)-transitively) fails
    try:
        def apply_perm(g, i):
            try:
                if i >= 0 and i < g.size:
                    return g(i)
            except Exception:
                pass
            return i

        def is_k_transitive(Grp, S, k_val):
            if k_val == 0:
                return True
            if k_val == 1:
                if not S:
                    return True
                S_set = set(S)
                x0 = next(iter(S_set))
                orbit = {x0}
                queue = [x0]
                gens = Grp.generators
                while queue:
                    curr = queue.pop(0)
                    for g in gens:
                        nxt = apply_perm(g, curr)
                        if nxt not in orbit and nxt in S_set:
                            orbit.add(nxt)
                            queue.append(nxt)
                return orbit == S_set
            else:
                if not S:
                    return False
                if not is_k_transitive(Grp, S, 1):
                    return False
                x0 = next(iter(S))
                if isinstance(x0, (int, sympy.Integer)):
                    x0_int = int(x0)
                    if x0_int >= 0 and x0_int < Grp.degree:
                        Grp_x0 = Grp.stabilizer(x0_int)
                    else:
                        Grp_x0 = Grp
                    S_minus_x0 = set(S) - {x0_int, x0}
                else:
                    Grp_x0 = Grp
                    S_minus_x0 = set(S) - {x0}
                return is_k_transitive(Grp_x0, S_minus_x0, k_val - 1)

        lhs = is_k_transitive(G, X, k)
        
        if isinstance(x, (int, sympy.Integer)):
            x_int = int(x)
            if x_int >= 0 and x_int < G.degree:
                Gx = G.stabilizer(x_int)
            else:
                Gx = G
            X_minus_x = X - {x_int, x}
        else:
            Gx = G
            X_minus_x = X - {x}
            
        rhs_part1 = is_k_transitive(G, X, 1)
        rhs_part2 = is_k_transitive(Gx, X_minus_x, k - 1)
        rhs = rhs_part1 and rhs_part2
        
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: k is an integer such that k >= 2",
    "H_3: X contains at least k elements",
    "¬Q: The equivalence between G acting k-transitively and (G acting transitively and G_x acting (k-1)-transitively) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3