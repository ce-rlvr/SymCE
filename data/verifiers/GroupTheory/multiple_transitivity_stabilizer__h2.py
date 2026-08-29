import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import itertools

# Top-level setup: named object bindings for witness expressions
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
    Checks if a permutation group G acts k-transitively on the set X.
    By standard mathematical convention, k-transitivity is only defined for k >= 1.
    """
    if k < 1:
        return False
    if len(X) < k:
        return False
    
    X_list = list(X)
    tuples = list(itertools.permutations(X_list, k))
    if not tuples:
        return True
        
    def apply_g(g, tup):
        # Apply permutation g to each element in the tuple.
        # Elements >= g.size are fixed by g.
        return tuple(g(i) if i < g.size else i for i in tup)
        
    t0 = tuples[0]
    orbit = set([t0])
    queue = [t0]
    
    gens = G.generators
    if not gens:
        gens = [Permutation()]
        
    while queue:
        curr = queue.pop(0)
        for g in gens:
            nxt = apply_g(g, curr)
            if nxt not in orbit:
                orbit.add(nxt)
                queue.append(nxt)
                if len(orbit) == len(tuples):
                    return True
    return len(orbit) == len(tuples)

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness should be a tuple: (G, X, k, x) or (G, k, x).
    """
    try:
        if len(witness) == 4:
            G, X, k, x = witness
        elif len(witness) == 3:
            G, k, x = witness
            X = set(range(G.degree))
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group acting on a set X
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            X_set = set(X)
            h1 = True
            # Check if X is invariant under the action of G
            for g in G.generators:
                for i in X_set:
                    val = g(i) if i < g.size else i
                    if val not in X_set:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False
        
    # H_2: X contains at least k elements
    try:
        h2 = len(X) >= k
    except Exception:
        h2 = False
        
    # H_3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False
        
    # ¬Q: The conclusion fails at the witness
    # Conclusion: G acts k-transitively on X iff G acts transitively on X and G_x acts (k-1)-transitively on X \ {x}
    try:
        # LHS: G acts k-transitively on X
        lhs = is_k_transitive(G, X, k)
        
        # RHS part 1: G acts transitively on X
        transitive_X = is_k_transitive(G, X, 1)
        
        # RHS part 2: G_x acts (k-1)-transitively on X \ {x}
        if x < G.degree:
            G_x = G.stabilizer(x)
        else:
            G_x = G
            
        X_minus_x = set(X) - {x}
        k_minus_1_transitive = is_k_transitive(G_x, X_minus_x, k - 1)
        
        rhs = transitive_X and k_minus_1_transitive
        
        # The conjecture claims LHS == RHS. We want the negation (LHS != RHS).
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: X contains at least k elements",
    "H_3: x is an element of X",
    "¬Q: The biconditional for k-transitivity fails"
]

N_HYP = 3
NEG_Q_INDEX = 3