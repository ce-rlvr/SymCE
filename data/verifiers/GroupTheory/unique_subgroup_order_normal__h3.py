import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: There is no other subgroup of G of order n besides H",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, H, n = witness
            elif len(witness) == 2:
                G, H = witness
                n = G.order() + 1
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if isinstance(H, list):
            H = PermutationGroup(H)
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        if h1 and isinstance(H, PermutationGroup):
            h2 = all(g in G for g in H.generators)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H_3: There is no other subgroup of G of order n besides H
    try:
        if not (h1 and h2 and isinstance(n, (int, sympy.Integer))):
            h3 = False
        else:
            if n <= 0:
                h3 = True
            elif G.order() % n != 0:
                h3 = True
            else:
                elements = list(G.generate())
                H_order = H.order()
                
                cyclic = set()
                for g in elements:
                    c = set()
                    curr = g
                    while curr not in c:
                        c.add(curr)
                        curr = curr * g
                    cyclic.add(frozenset(c))
                    
                known = set(cyclic)
                queue = list(cyclic)
                
                h3 = True
                for C in known:
                    if len(C) == n:
                        if n != H_order or any(c not in H for c in C):
                            h3 = False
                            break
                            
                if h3:
                    while queue:
                        A = queue.pop(0)
                        for B in cyclic:
                            if B.issubset(A):
                                continue
                            sub = set(A)
                            frontier = list(B)
                            while frontier:
                                new_frontier = []
                                for x in frontier:
                                    for y in list(sub):
                                        xy = x * y
                                        if xy not in sub:
                                            sub.add(xy)
                                            new_frontier.append(xy)
                                        yx = y * x
                                        if yx not in sub:
                                            sub.add(yx)
                                            new_frontier.append(yx)
                                frontier = new_frontier
                            C = frozenset(sub)
                            if C not in known:
                                known.add(C)
                                queue.append(C)
                                if len(C) == n:
                                    if n != H_order or any(c not in H for c in C):
                                        h3 = False
                                        break
                        if not h3:
                            break
    except Exception:
        h3 = False
        
    # neg_Q: H is not a normal subgroup of G
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            is_normal = True
            for g in G.generators:
                for h in H.generators:
                    if (g * h * ~g) not in H:
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = not is_normal
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]