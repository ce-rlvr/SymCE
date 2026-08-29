import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup, Permutation

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

def is_k_transitive(G, X, k):
    """
    Checks if G acts k-transitively on X.
    By definition, this means G has exactly one orbit on the set of k-tuples of distinct elements.
    If the set of k-tuples is empty (i.e., |X| < k), the condition 'for all pairs of k-tuples...'
    is vacuously true, which is exactly why the dropped hypothesis |X| >= k is necessary.
    """
    tuples = list(itertools.permutations(X, k))
    if not tuples:
        return True
    
    t1 = tuples[0]
    orbit = {t1}
    queue = [t1]
    gens = G.generators
    
    while queue:
        curr = queue.pop(0)
        for g in gens:
            nxt = tuple(g(x) for x in curr)
            if nxt not in orbit:
                orbit.add(nxt)
                queue.append(nxt)
                
    return len(orbit) == len(tuples)

def get_stabilizer(G, x):
    """
    Safely gets the stabilizer of x in G.
    SymPy's G.stabilizer(x) requires 0 <= x < G.degree.
    If x is outside this range, it is implicitly fixed by all permutations in G.
    """
    if 0 <= x < G.degree:
        return G.stabilizer(x)
    else:
        return G

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if len(witness) == 2:
            G, k = witness
            X = list(range(G.degree))
        elif len(witness) == 3:
            G, X, k = witness
            X = list(set(X))
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: X is a set with at least two elements
    try:
        h2 = len(X) >= 2
    except Exception:
        h2 = False

    # H_3: G acts on X
    try:
        h3 = True
        for g in G.generators:
            for x in X:
                if g(x) not in X:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # ¬Q: G acts k-transitively on X iff G acts transitively on X and for any x in X, G_x acts (k-1)-transitively on X \ {x}
    try:
        k = int(k)
        if k < 1:
            neg_q = False
        else:
            lhs = is_k_transitive(G, X, k)
            
            rhs_part1 = is_k_transitive(G, X, 1)
            rhs_part2 = True
            for x in X:
                Gx = get_stabilizer(G, x)
                X_minus_x = [y for y in X if y != x]
                if not is_k_transitive(Gx, X_minus_x, k - 1):
                    rhs_part2 = False
                    break
            rhs = rhs_part1 and rhs_part2
            
            # The conjecture is FALSE at the witness if the equivalence fails
            neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set with at least two elements",
    "H_3: G acts on X",
    "¬Q: G acts k-transitively on X iff G acts transitively on X and for any x in X, G_x acts (k-1)-transitively on X \\ {x} (fails)"
]

N_HYP = 3
NEG_Q_INDEX = 3