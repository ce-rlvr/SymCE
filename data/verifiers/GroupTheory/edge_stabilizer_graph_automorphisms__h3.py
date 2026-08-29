import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness references
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
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple: (n, E, e_idx)
    where:
      - n is the number of vertices (0 to n-1)
      - E is a list of edges, where each edge is a tuple of two vertices (u, v)
      - e_idx is the index of the chosen edge e in E
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False]
        n, E, e_idx = witness
        
        if not isinstance(n, int) or n <= 0 or n > 8:
            return [False, False]
        if not isinstance(E, (list, tuple)):
            return [False, False]
        if not all(isinstance(edge, (list, tuple)) and len(edge) == 2 for edge in E):
            return [False, False]
        if not all(isinstance(u, int) and isinstance(v, int) and 0 <= u < n and 0 <= v < n for u, v in E):
            return [False, False]
        if not isinstance(e_idx, int) or not (0 <= e_idx < len(E)):
            return [False, False]
            
        # Normalize edges to be undirected
        E_norm = [tuple(sorted(edge)) for edge in E]
        
        # H1: Gamma is an undirected graph
        h1 = True
    except Exception:
        return [False, False]
        
    try:
        m = len(E_norm)
        if m > 8: # Prevent timeout for large edge sets
            return [False, False]
            
        G = []
        E_sorted = sorted(E_norm)
        
        # Precompute degrees to quickly filter invalid vertex permutations
        degrees = [0] * n
        for u, v in E_norm:
            degrees[u] += 1
            degrees[v] += 1
            
        # Compute G = Aut(Gamma) acting on V and E
        for sigma in itertools.permutations(range(n)):
            if any(degrees[i] != degrees[sigma[i]] for i in range(n)):
                continue
                
            mapped_E = [tuple(sorted((sigma[u], sigma[v]))) for u, v in E_norm]
            if sorted(mapped_E) != E_sorted:
                continue
                
            # Find all valid edge permutations tau for this sigma
            indices_by_type = {}
            for idx, edge in enumerate(E_norm):
                indices_by_type.setdefault(edge, []).append(idx)
                
            tau_assignments = []
            for edge_type, J in indices_by_type.items():
                I = [i for i, e in enumerate(mapped_E) if e == edge_type]
                bijections = []
                for p in itertools.permutations(J):
                    bijections.append(list(zip(I, p)))
                tau_assignments.append(bijections)
                
            for combo in itertools.product(*tau_assignments):
                tau = [0] * m
                for assignment in combo:
                    for i, j in assignment:
                        tau[i] = j
                G.append((sigma, tuple(tau)))
                
        u, v = E_norm[e_idx]
        
        # G_e: stabilizer of the edge e
        G_e = [g for g in G if g[1][e_idx] == e_idx]
        
        # G_u \cap G_v: intersection of vertex stabilizers
        G_u_cap_v = [g for g in G if g[0][u] == u and g[0][v] == v]
        
        # Check if G_u \cap G_v is a subgroup of G_e
        # (If it is a subgroup, it is mathematically guaranteed to be normal and of index <= 2)
        is_subgroup = True
        G_e_set = set(G_e)
        for g in G_u_cap_v:
            if g not in G_e_set:
                is_subgroup = False
                break
                
        # The conclusion FAILS if it is NOT a subgroup
        neg_q = not is_subgroup
                
    except Exception:
        return [False, False]
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Gamma is an undirected graph",
    "¬Q: G_e does not contain G_u \\cap G_v as a normal subgroup of index at most 2"
]

N_HYP = 1
NEG_Q_INDEX = 1