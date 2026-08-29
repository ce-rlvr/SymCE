import itertools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def apply_g(g, c):
    try:
        return g(c)
    except Exception:
        pass
    try:
        return g.get(c, c)
    except Exception:
        pass
    try:
        return c ^ g
    except Exception:
        pass
    return c

def acts_k_transitively(group_elems, domain, degree):
    if degree == 0:
        return True
    domain_list = list(domain)
    if len(domain_list) < degree:
        return True
    
    for g in group_elems:
        for c in domain_list:
            if apply_g(g, c) not in domain_list:
                return False
    
    tuples = list(itertools.permutations(domain_list, degree))
    for t1 in tuples:
        for t2 in tuples:
            found = False
            for g in group_elems:
                if tuple(apply_g(g, c) for c in t1) == t2:
                    found = True
                    break
            if not found:
                return False
    return True

def conditions(witness) -> list[bool]:
    k = witness.get('k')
    X = witness.get('X')
    x = witness.get('x')
    G = witness.get('G')

    try:
        h1 = isinstance(k, int) and k >= 2
    except Exception:
        h1 = False

    try:
        h2 = len(list(X)) >= k
    except Exception:
        h2 = False

    try:
        h3 = x in list(X)
    except Exception:
        h3 = False

    try:
        try:
            G_elems = list(G)
        except TypeError:
            if hasattr(G, 'elements'):
                G_elems = list(G.elements)
            elif hasattr(G, 'generate'):
                G_elems = list(G.generate())
            else:
                G_elems = []

        A = acts_k_transitively(G_elems, X, k)
        B = acts_k_transitively(G_elems, X, 1)
        
        G_x = [g for g in G_elems if apply_g(g, x) == x]
        X_minus_x = [c for c in list(X) if c != x]
        
        C = acts_k_transitively(G_x, X_minus_x, k - 1)
        
        neg_q = not (A == (B and C))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: k is an integer such that k >= 2",
    "H_2: X contains at least k elements",
    "H_3: x is an element of X",
    "¬Q: G acts k-transitively on X iff G acts transitively on X and G_x acts (k-1)-transitively on X \\setminus {x}"
]

N_HYP = 3
NEG_Q_INDEX = 3