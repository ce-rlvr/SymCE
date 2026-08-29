import itertools
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_k_transitive(G, X, k):
    """
    Evaluates if a permutation group G acts k-transitively on a set X.
    Uses the definition that allows vacuous truth if |X| < k, which is 
    necessary to expose the falsehood of the conjecture when the |X| >= k 
    hypothesis is dropped.
    """
    if k == 0:
        return True
    tuples = list(itertools.permutations(X, k))
    if not tuples:
        return True
    
    orbit = set()
    t0 = tuples[0]
    queue = [t0]
    orbit.add(t0)
    gens = G.generators
    head = 0
    
    while head < len(queue):
        curr = queue[head]
        head += 1
        for g in gens:
            nxt = tuple(g(x) for x in curr)
            if nxt not in orbit:
                orbit.add(nxt)
                queue.append(nxt)
                if len(orbit) == len(tuples):
                    return True
                    
    return len(orbit) == len(tuples)

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if len(witness) == 3:
            G, X, k = witness
        elif len(witness) == 2:
            G, k = witness
            X = list(range(G.degree))
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G acts on X
    try:
        if h1:
            X_tuple = tuple(X)
            X_set = set(X_tuple)
            acts = True
            for g in G.generators:
                for x in X_tuple:
                    if g(x) not in X_set:
                        acts = False
                        break
                if not acts:
                    break
            h2 = acts
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: k is an integer strictly greater than 1
    try:
        h3 = isinstance(k, int) and k > 1
    except Exception:
        h3 = False

    # ¬Q: The conclusion fails at the witness
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            X_tuple = tuple(X)
            
            # Left-hand side: G acts k-transitively on X
            lhs = is_k_transitive(G, X_tuple, k)
            
            # Right-hand side: G acts transitively on X AND for any x in X, G_x acts (k-1)-transitively on X \ {x}
            rhs_part1 = is_k_transitive(G, X_tuple, 1)
            rhs_part2 = True
            for x in X_tuple:
                Gx = G.stabilizer(x)
                X_minus_x = tuple(y for y in X_tuple if y != x)
                if not is_k_transitive(Gx, X_minus_x, k - 1):
                    rhs_part2 = False
                    break
            rhs = rhs_part1 and rhs_part2
            
            # The conjecture claims lhs == rhs. It fails if lhs != rhs.
            neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X",
    "H_3: k is an integer strictly greater than 1",
    "¬Q: G acts k-transitively on X is NOT equivalent to (G acts transitively on X and for any x in X, G_x acts (k-1)-transitively on X \\ {x})"
]

N_HYP = 3
NEG_Q_INDEX = 3