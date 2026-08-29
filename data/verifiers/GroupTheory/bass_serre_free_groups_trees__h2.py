import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup,
    CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts freely on the vertices and edges of T",
    "H_3: G acts without inversions on T",
    "¬Q: G is not a free group"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            V = witness.get('vertices', [])
            E = witness.get('edges', [])
        else:
            G, V, E = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        E_sets = []
        for e in E:
            e_list = list(e)
            if not e_list:
                continue
            u = e_list[0]
            v = e_list[1] if len(e_list) > 1 else e_list[0]
            E_sets.append(frozenset([u, v]))
        E_set = set(E_sets)
        V_set = set(V)
    except Exception:
        E_sets = []
        E_set = set()
        V_set = set()

    def is_automorphism(g):
        for v in V_set:
            try:
                if g(v) not in V_set: 
                    return False
            except Exception:
                return False
        for e in E_sets:
            l = list(e)
            u = l[0]
            v = l[1] if len(l) > 1 else l[0]
            try:
                if frozenset([g(u), g(v)]) not in E_set:
                    return False
            except Exception:
                return False
        return True

    try:
        h2 = True
        if h1 and V_set:
            for e in E_sets:
                if not e.issubset(V_set):
                    h2 = False
                    break
            if h2:
                for g in G.elements:
                    if not is_automorphism(g):
                        h2 = False
                        break
                    if g.is_Identity:
                        continue
                    for v in V_set:
                        if g(v) == v:
                            h2 = False
                            break
                    if not h2: 
                        break
                    for e in E_sets:
                        l = list(e)
                        u = l[0]
                        v = l[1] if len(l) > 1 else l[0]
                        if frozenset([g(u), g(v)]) == e:
                            h2 = False
                            break
                    if not h2: 
                        break
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        h3 = True
        if h1 and V_set:
            for e in E_sets:
                if not e.issubset(V_set):
                    h3 = False
                    break
            if h3:
                for g in G.elements:
                    if not is_automorphism(g):
                        h3 = False
                        break
                    for e in E_sets:
                        l = list(e)
                        u = l[0]
                        v = l[1] if len(l) > 1 else l[0]
                        if u != v and g(u) == v and g(v) == u:
                            h3 = False
                            break
                    if not h3: 
                        break
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        neg_q = False
        if h1:
            # In SymPy, PermutationGroups are finite. 
            # The only finite free group is the trivial group (rank 0).
            neg_q = (G.order() > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]