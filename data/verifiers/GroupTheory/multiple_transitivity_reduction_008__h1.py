import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation(0)])

def parse_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) == 2:
            G, k = witness
            if hasattr(G, 'degree'):
                X = list(range(G.degree))
                if G.degree < 2:
                    X = [0, 1]
            else:
                X = []
            return G, X, k
        elif len(witness) == 3:
            G, X, k = witness
            return G, list(X), k
    return None, None, None

def get_stabilizer(G, x):
    try:
        if x >= G.degree:
            return G
        return G.stabilizer(x)
    except Exception:
        return G

def is_k_transitive(G, domain, k):
    tuples = list(itertools.permutations(domain, k))
    if not tuples:
        return True
    
    start = tuples[0]
    orbit = set([start])
    queue = [start]
    gens = G.generators
    
    while queue:
        curr = queue.pop(0)
        for g in gens:
            next_tup = []
            for x in curr:
                try:
                    next_tup.append(g(x))
                except Exception:
                    next_tup.append(x)
            next_tup = tuple(next_tup)
            
            if next_tup not in orbit:
                orbit.add(next_tup)
                queue.append(next_tup)
                if len(orbit) == len(tuples):
                    return True
    return len(orbit) == len(tuples)

def is_transitive(G, domain):
    return is_k_transitive(G, domain, 1)

def conditions(witness):
    G, X, k = parse_witness(witness)
    if G is None:
        return [False, False, False, False]
    
    # H1: X is a set with at least two elements
    try:
        h1 = len(X) >= 2
    except Exception:
        h1 = False
        
    # H2: G acts on X
    try:
        if not isinstance(G, PermutationGroup):
            h2 = False
        else:
            h2 = True
            for g in G.generators:
                for x in X:
                    try:
                        res = g(x)
                    except Exception:
                        res = x
                    if res not in X:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False
        
    # H3: k is an integer strictly greater than 1
    try:
        h3 = isinstance(k, int) and k > 1
    except Exception:
        h3 = False
        
    # neg_Q: Conclusion fails
    try:
        lhs = is_k_transitive(G, X, k)
        
        rhs_part1 = is_transitive(G, X)
        rhs_part2 = True
        for x in X:
            G_x = get_stabilizer(G, x)
            X_minus_x = [y for y in X if y != x]
            if not is_k_transitive(G_x, X_minus_x, k - 1):
                rhs_part2 = False
                break
        rhs = rhs_part1 and rhs_part2
        
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set with at least two elements",
    "H_2: G acts on X",
    "H_3: k is an integer strictly greater than 1",
    "¬Q: The equivalence between k-transitivity and the stabilizer condition fails"
]

N_HYP = 3
NEG_Q_INDEX = 3