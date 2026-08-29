import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                R, G = witness
            else:
                return [False, False, False, False]
        else:
            R = None
            G = witness

        H1 = True
        H2 = hasattr(G, 'elements')
        H3 = True

        if not H2:
            return [H1, H2, H3, False]

        elements = list(G.elements)
        n = len(elements)
        if n == 0:
            return [H1, H2, H3, False]

        parent = {e: e for e in elements}
        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j

        for g in elements:
            for x in elements:
                try:
                    xg = x * g
                except Exception:
                    continue
                if xg in parent:
                    union(x, xg)
        
        components = len(set(find(e) for e in elements))
        rank = n - components
        neg_Q = bool(rank != n - 1)

        return [H1, H2, H3, neg_Q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: G is a group",
    "H_3: The group ring of G over R",
    "¬Q: The kernel of epsilon is not generated as an ideal by the set {g - 1 | g in G}"
]

N_HYP = 3
NEG_Q_INDEX = 3