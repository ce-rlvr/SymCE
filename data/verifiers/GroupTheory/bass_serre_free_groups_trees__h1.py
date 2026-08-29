import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup
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

def conditions(witness):
    try:
        G = witness['G']
        V_raw = list(witness['V'])
        V = V_raw
        E = list(witness['E'])
        action_obj = witness['action']
        
        if callable(action_obj):
            action = action_obj
        else:
            action = lambda g, x: action_obj[(g, x)]
    except Exception:
        return [False, False, False, False]

    # H1: T is a tree
    try:
        if len(V) != len(set(V)):
            h1 = False
        elif len(V) == 0 and len(E) == 0:
            h1 = True
        elif len(V) != len(E) + 1:
            h1 = False
        else:
            visited = set()
            def dfs(v):
                visited.add(v)
                for e in E:
                    e_list = list(e)
                    if len(e_list) != 2:
                        continue
                    if v == e_list[0]:
                        u = e_list[1]
                    elif v == e_list[1]:
                        u = e_list[0]
                    else:
                        continue
                    if u not in visited:
                        dfs(u)
            dfs(V[0])
            h1 = (visited == set(V))
            
            if h1:
                for e in E:
                    e_list = list(e)
                    if e_list[0] not in V or e_list[1] not in V:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: G acts freely on the vertices and edges of T
    try:
        h2 = True
        elements = list(G.elements) if hasattr(G, 'elements') else list(G)
        if hasattr(G, 'identity'):
            identity = G.identity
        else:
            identity = Permutation()
            
        # Check homomorphism property
        for g in elements:
            for h in elements:
                gh = g * h
                for v in V:
                    if action(gh, v) != action(g, action(h, v)):
                        h2 = False
                        break
                if not h2:
                    break
            if not h2:
                break

        if h2:
            for g in elements:
                is_id = (g == identity) or (hasattr(g, 'is_identity') and g.is_identity)
                
                for v in V:
                    gv = action(g, v)
                    if gv not in V:
                        h2 = False
                        break
                    if is_id and gv != v:
                        h2 = False
                        break
                    if not is_id and gv == v:
                        h2 = False
                        break
                if not h2:
                    break
                    
                for e in E:
                    e_list = list(e)
                    if len(e_list) != 2:
                        continue
                    u, v = e_list[0], e_list[1]
                    gu = action(g, u)
                    gv = action(g, v)
                    
                    mapped_edge = {gu, gv}
                    edge_in_E = False
                    for edge in E:
                        if set(edge) == mapped_edge:
                            edge_in_E = True
                            break
                    if not edge_in_E:
                        h2 = False
                        break
                        
                    if is_id:
                        if not ((gu == u and gv == v) or (gu == v and gv == u)):
                            h2 = False
                            break
                    else:
                        if (gu == u and gv == v) or (gu == v and gv == u):
                            h2 = False
                            break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: G acts without inversions on T
    try:
        h3 = True
        elements = list(G.elements) if hasattr(G, 'elements') else list(G)
        for g in elements:
            for e in E:
                e_list = list(e)
                if len(e_list) != 2:
                    continue
                u, v = e_list[0], e_list[1]
                gu = action(g, u)
                gv = action(g, v)
                if gu == v and gv == u:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # neg_Q: G is not a free group
    try:
        is_free = False
        if hasattr(G, 'order'):
            try:
                if G.order() == 1:
                    is_free = True
            except Exception:
                pass
        if hasattr(G, 'relators'):
            if len(G.relators) == 0:
                is_free = True
        neg_q = not is_free
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: T is a tree",
    "H_2: G acts freely on the vertices and edges of T",
    "H_3: G acts without inversions on T",
    "¬Q: G is not a free group"
]

N_HYP = 3
NEG_Q_INDEX = 3