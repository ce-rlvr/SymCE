import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

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

def conditions(witness) -> list[bool]:
    try:
        G, X, k, x = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group acting on a set X
    try:
        h1_ok = False
        if isinstance(G, PermutationGroup) and isinstance(X, (list, set, tuple)):
            X_set = set(X)
            if all(isinstance(c, int) and c >= 0 for c in X_set):
                acts = True
                for g in G.generators:
                    for c in X_set:
                        if g(c) not in X_set:
                            acts = False
                            break
                    if not acts:
                        break
                h1_ok = acts
    except Exception:
        h1_ok = False

    # H_2: k is an integer such that k \ge 2
    try:
        h2_ok = isinstance(k, int) and k >= 2
    except Exception:
        h2_ok = False

    # H_3: x is an element of X
    try:
        h3_ok = x in X
    except Exception:
        h3_ok = False

    # ¬Q: The conclusion fails at the witness
    try:
        def is_k_transitive(grp, domain, m):
            tuples = list(itertools.permutations(domain, m))
            if not tuples:
                # Vacuously true if there are no m-tuples
                return True
            t1 = tuples[0]
            orbit = set([t1])
            queue = [t1]
            gens = grp.generators if hasattr(grp, 'generators') else grp
            while queue:
                curr = queue.pop(0)
                for g in gens:
                    nxt = tuple(g(c) for c in curr)
                    if nxt not in orbit:
                        orbit.add(nxt)
                        queue.append(nxt)
            return len(orbit) == len(tuples)

        lhs = is_k_transitive(G, X, k)
        
        transitive_G = is_k_transitive(G, X, 1)
        Gx = G.stabilizer(x)
        X_minus_x = [c for c in X if c != x]
        Gx_transitive = is_k_transitive(Gx, X_minus_x, k - 1)
        
        rhs = transitive_G and Gx_transitive
        
        neg_q_ok = (lhs != rhs)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: k is an integer such that k >= 2",
    "H_3: x is an element of X",
    "¬Q: G acts k-transitively on X iff G acts transitively on X and G_x acts (k-1)-transitively on X \\ {x} is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3