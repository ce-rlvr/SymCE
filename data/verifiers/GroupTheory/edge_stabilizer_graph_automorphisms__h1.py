import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from itertools import permutations

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    witness is expected to be a tuple (V, E, e) representing a graph (possibly a multigraph), where:
      - V is a list/set/tuple of vertices.
      - E is a list/set/tuple of edges. To support multigraphs, each edge should be a tuple 
        with at least 2 elements (u, v, ...) where u and v are the endpoints in V.
      - e is the specific edge in E to be tested.
    """
    try:
        V, E, e = witness
        
        if not isinstance(V, (list, set, tuple)): 
            return [False, False, False]
        if not isinstance(E, (list, set, tuple)): 
            return [False, False, False]
        
        V_list = list(V)
        E_list = list(E)
        
        # Edges must be unique objects (e.g. by including an edge ID) to properly define the action on E
        if len(set(E_list)) != len(E_list):
            return [False, False, False]
            
        # Check that all edges are valid and have endpoints in V
        valid_E = True
        for edge in E_list:
            if len(edge) < 2:
                valid_E = False
                break
            if edge[0] not in V_list or edge[1] not in V_list:
                valid_E = False
                break
        if not valid_E:
            return [False, False, False]
            
        h1 = True
        h2 = e in E_list
        
        if not (h1 and h2):
            return [h1, h2, False]
            
        # To avoid timeout, limit the size of V and E
        if len(V_list) > 5 or len(E_list) > 5:
            return [False, False, False]
            
        # Compute G = Aut(\Gamma) acting naturally on V and E
        auts = []
        for pV_vals in permutations(V_list):
            pV = dict(zip(V_list, pV_vals))
            for pE_vals in permutations(E_list):
                pE = dict(zip(E_list, pE_vals))
                
                valid = True
                for edge in E_list:
                    mapped_edge = pE[edge]
                    orig_endpoints = {pV[edge[0]], pV[edge[1]]}
                    mapped_endpoints = {mapped_edge[0], mapped_edge[1]}
                    if orig_endpoints != mapped_endpoints:
                        valid = False
                        break
                if valid:
                    auts.append((pV, pE))
                    
        u, v = e[0], e[1]
        
        # G_e: stabilizer of the edge e
        G_e = [g for g in auts if g[1][e] == e]
        
        # G_u \cap G_v: intersection of vertex stabilizers
        G_u_cap_G_v = [g for g in auts if g[0][u] == u and g[0][v] == v]
        
        # Check if G_u \cap G_v is a subset of G_e
        subset = all(g in G_e for g in G_u_cap_G_v)
        
        # Check if G_u \cap G_v is a normal subgroup of G_e
        normal = True
        if subset:
            for h in G_u_cap_G_v:
                for g in G_e:
                    pV_g, pE_g = g
                    pV_h, pE_h = h
                    
                    pV_g_inv = {val: key for key, val in pV_g.items()}
                    
                    # Compute the action of g * h * g^-1 on the vertices
                    pV_res = {x: pV_g[pV_h[pV_g_inv[x]]] for x in V_list}
                    
                    # If it doesn't fix u and v, it's not in G_u \cap G_v
                    if pV_res[u] != u or pV_res[v] != v:
                        normal = False
                        break
                if not normal:
                    break
                    
        # Check if the index is at most 2
        index_at_most_2 = False
        if subset and normal:
            if len(G_u_cap_G_v) > 0:
                index = len(G_e) // len(G_u_cap_G_v)
                if index <= 2:
                    index_at_most_2 = True
                    
        conclusion = subset and normal and index_at_most_2
        neg_q = not conclusion
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G = Aut(\\Gamma) is the automorphism group of \\Gamma acting naturally on V and E",
    "H_2: e = \\{u, v\\} is an edge in E",
    "¬Q: G_e does not contain G_u \\cap G_v as a normal subgroup of index at most 2"
]

N_HYP = 2
NEG_Q_INDEX = 2