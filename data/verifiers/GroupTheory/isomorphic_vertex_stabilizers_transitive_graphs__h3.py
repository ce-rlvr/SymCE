import sympy
from sympy.combinatorics import Permutation, PermutationGroup
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

def is_graph(witness):
    if not isinstance(witness, dict): return False
    if 'V' not in witness or 'E' not in witness: return False
    V = witness['V']
    E = witness['E']
    if not isinstance(V, (list, set, tuple)): return False
    if not isinstance(E, (list, set, tuple)): return False
    for edge in E:
        if not isinstance(edge, (list, set, tuple)) or len(edge) != 2: return False
        u, v = tuple(edge)
        if u not in V or v not in V: return False
    return True

def get_automorphism_group(V, E):
    n = len(V)
    if n == 0:
        return PermutationGroup([Permutation()]), [], {}
    v_list = list(V)
    v_map = {v: i for i, v in enumerate(v_list)}
    
    adj = {i: set() for i in range(n)}
    for edge in E:
        u, v = edge
        if u in v_map and v in v_map:
            adj[v_map[u]].add(v_map[v])
            adj[v_map[v]].add(v_map[u])
            
    aut_perms = []
    
    def search(mapping, used):
        if len(mapping) == n:
            aut_perms.append(Permutation([mapping[i] for i in range(n)]))
            return
        
        u = len(mapping)
        u_adj = adj[u]
        
        for v in range(n):
            if not used[v]:
                if len(adj[u]) != len(adj[v]):
                    continue
                if (u in u_adj) != (v in adj[v]):
                    continue
                consistent = True
                for x in range(u):
                    if (x in u_adj) != (mapping[x] in adj[v]):
                        consistent = False
                        break
                if consistent:
                    mapping[u] = v
                    used[v] = True
                    search(mapping, used)
                    used[v] = False
                    del mapping[u]

    search({}, [False]*n)
    
    if not aut_perms:
        aut_perms = [Permutation(n-1 if n > 0 else 0)]
    return PermutationGroup(aut_perms), v_list, v_map

def is_vertex_transitive(witness):
    if not is_graph(witness): return False
    V = witness['V']
    E = witness['E']
    if not V: return True
    G, v_list, v_map = get_automorphism_group(V, E)
    orbit = G.orbit(0)
    return len(orbit) == len(V)

def get_stabilizer(G, element, v_map):
    if element in v_map:
        # It's a single vertex
        mapped_v = v_map[element]
        return G.stabilizer(mapped_v)
    elif isinstance(element, (tuple, list, set, frozenset)):
        # It's a set of vertices (e.g., an edge)
        mapped_set = set(v_map[x] for x in element)
        stab_perms = []
        for p in G.elements:
            if set(p(x) for x in mapped_set) == mapped_set:
                stab_perms.append(p)
        if not stab_perms:
            stab_perms = [Permutation(G.degree - 1 if G.degree > 0 else 0)]
        return PermutationGroup(stab_perms)
    else:
        raise KeyError(f"Element {element} not found in graph vertices")

def are_isomorphic(G1, G2):
    if G1.order() != G2.order():
        return False
    if G1.is_abelian != G2.is_abelian:
        return False
    if G1.order() > 1000:
        if hasattr(G1, 'is_isomorphic'):
            try:
                return G1.is_isomorphic(G2)
            except Exception:
                pass
        return True
    orders1 = sorted([g.order() for g in G1.elements])
    orders2 = sorted([g.order() for g in G2.elements])
    if orders1 != orders2:
        return False
    if hasattr(G1, 'is_isomorphic'):
        try:
            return G1.is_isomorphic(G2)
        except Exception:
            pass
    return True

def neg_conclusion(witness):
    if not is_graph(witness): return False
    if 'u' not in witness or 'v' not in witness: return False
    V = witness['V']
    E = witness['E']
    u = witness['u']
    v = witness['v']
    G, v_list, v_map = get_automorphism_group(V, E)
    stab_u = get_stabilizer(G, u, v_map)
    stab_v = get_stabilizer(G, v, v_map)
    return not are_isomorphic(stab_u, stab_v)

def conditions(witness):
    try:
        h1 = is_graph(witness)
    except Exception:
        h1 = False

    try:
        h2 = is_vertex_transitive(witness)
    except Exception:
        h2 = False

    try:
        neg_q = neg_conclusion(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Γ is a graph",
    "H_2: The automorphism group Aut(Γ) acts transitively on the vertex set V(Γ)",
    "¬Q: The point stabilizer of u in Aut(Γ) is NOT isomorphic as a group to the point stabilizer of v in Aut(Γ)"
]

N_HYP = 2
NEG_Q_INDEX = 2