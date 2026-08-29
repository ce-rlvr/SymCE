import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def apply_perm(p, i):
    try:
        return p(i) if i < p.size else i
    except Exception:
        return i

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If G acts without inversions on a tree T, then G is a free group."
    
    Expected witness format: (G, n, E)
      - G: A SymPy PermutationGroup
      - n: Number of vertices in the tree (vertices are 0, ..., n-1)
      - E: List/set of edges, where each edge is a pair of vertices
    """
    # H_1: G is a group
    try:
        G = witness[0]
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: T is a tree
    try:
        _, n, E = witness
        h2 = False
        if isinstance(n, int) and n > 0 and isinstance(E, (list, set, tuple)):
            valid_edges = True
            for edge in E:
                if not (isinstance(edge, (list, tuple, set, frozenset)) and len(edge) == 2):
                    valid_edges = False
                    break
                u, v = tuple(edge)
                if not (isinstance(u, int) and isinstance(v, int) and 0 <= u < n and 0 <= v < n and u != v):
                    valid_edges = False
                    break
            
            if valid_edges and len(E) == n - 1:
                # Check if the graph is connected
                adj = {i: [] for i in range(n)}
                for edge in E:
                    u, v = tuple(edge)
                    adj[u].append(v)
                    adj[v].append(u)
                
                visited = set()
                q = [0]
                visited.add(0)
                while q:
                    curr = q.pop(0)
                    for neighbor in adj[curr]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            q.append(neighbor)
                
                if len(visited) == n:
                    h2 = True
    except Exception:
        h2 = False

    # H_3: G acts without inversions on T
    try:
        G, n, E = witness
        h3 = False
        if h1 and h2:
            acts = True
            E_set = {frozenset(edge) for edge in E}
            
            # Check if G acts on T (preserves vertices and edges)
            for g in G.generators:
                for i in range(n):
                    if apply_perm(g, i) >= n:
                        acts = False
                        break
                if not acts: break
                
                for edge in E:
                    u, v = tuple(edge)
                    gu = apply_perm(g, u)
                    gv = apply_perm(g, v)
                    if frozenset((gu, gv)) not in E_set:
                        acts = False
                        break
                if not acts: break
            
            if acts:
                # Check if G acts without inversions
                # For a finite tree, this is equivalent to no edge having its endpoints in the same orbit.
                orbit_dict = {}
                orbits = G.orbits()
                for i, orb in enumerate(orbits):
                    for v in orb:
                        orbit_dict[v] = i
                
                next_orbit_id = len(orbits)
                for v in range(n):
                    if v not in orbit_dict:
                        orbit_dict[v] = next_orbit_id
                        next_orbit_id += 1
                
                without_inversions = True
                for edge in E:
                    u, v = tuple(edge)
                    if orbit_dict[u] == orbit_dict[v]:
                        without_inversions = False
                        break
                
                h3 = without_inversions
    except Exception:
        h3 = False

    # ¬Q: G is not a free group
    try:
        G = witness[0]
        if isinstance(G, PermutationGroup):
            # The only finite free group is the trivial group (rank 0).
            # Thus, a finite group is not a free group iff its order is > 1.
            neg_q = G.order() > 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: T is a tree",
    "H_3: G acts without inversions on T",
    "¬Q: G is not a free group"
]

N_HYP = 3
NEG_Q_INDEX = 3