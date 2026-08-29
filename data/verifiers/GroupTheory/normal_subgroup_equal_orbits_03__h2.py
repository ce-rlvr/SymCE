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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts transitively on X",
    "H_3: N is a normal subgroup of G",
    "¬Q: Not all orbits of N on X have the same cardinality"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, N = witness
                if hasattr(G, 'degree'):
                    X = list(range(G.degree))
                else:
                    X = []
            elif len(witness) == 3:
                G, X, N = witness
                X = list(X)
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: G acts transitively on X
    try:
        if not X:
            h2 = False
        else:
            x0 = list(X)[0]
            orbit = {x0}
            queue = [x0]
            while queue:
                curr = queue.pop(0)
                for g in G.generators:
                    nxt = g(curr) if curr < g.size else curr
                    if nxt not in orbit:
                        orbit.add(nxt)
                        queue.append(nxt)
            h2 = (orbit == set(X))
    except Exception:
        h2 = False

    # H3: N is a normal subgroup of G
    try:
        h3 = bool(N.is_normal(G))
    except Exception:
        h3 = False

    # neg_Q: Not all orbits of N on X have the same cardinality
    try:
        elements = set(X)
        orbits = []
        while elements:
            x = elements.pop()
            orbit = {x}
            queue = [x]
            while queue:
                curr = queue.pop(0)
                for n in N.generators:
                    nxt = n(curr) if curr < n.size else curr
                    if nxt in elements:
                        elements.remove(nxt)
                        orbit.add(nxt)
                        queue.append(nxt)
            orbits.append(orbit)
        
        lengths = {len(o) for o in orbits}
        neg_q = len(lengths) > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]