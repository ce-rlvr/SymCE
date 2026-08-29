import itertools
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
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

def landau_g(n):
    """Computes the maximum order of a permutation of degree n (Landau's function)."""
    if n <= 0: return 1
    dp = [1] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        is_p = True
        for p in primes:
            if p * p > i: break
            if i % p == 0:
                is_p = False
                break
        if is_p: primes.append(i)
        
    for p in primes:
        for i in range(n, -1, -1):
            pk = p
            while pk <= i:
                dp[i] = max(dp[i], dp[i - pk] * pk)
                pk *= p
    return dp[n]

def is_aut_cyclic(G):
    """Checks if the automorphism group of G is cyclic."""
    try:
        elements = list(G.generate())
    except AttributeError:
        return False
        
    n = len(elements)
    if n <= 2:
        return True
        
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    mult = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            prod = elements[i] * elements[j]
            mult[i][j] = elem_to_idx[prod]
            
    gens = G.generators
    gens_idx = [elem_to_idx[g] for g in gens]
    
    id_idx = elem_to_idx[G.identity]
    bfs_tree = []
    visited = {id_idx}
    queue = [id_idx]
    
    # Build a spanning tree to quickly evaluate homomorphisms
    while queue:
        curr = queue.pop(0)
        for gen_pos, g_idx in enumerate(gens_idx):
            nxt = mult[curr][g_idx]
            if nxt not in visited:
                visited.add(nxt)
                bfs_tree.append((curr, gen_pos, nxt))
                queue.append(nxt)
                
    orders = [elements[i].order() for i in range(n)]
    gen_orders = [orders[i] for i in range(len(gens_idx))]
    
    valid_targets = []
    for go in gen_orders:
        valid_targets.append([i for i in range(n) if orders[i] == go])
        
    # Aut(G) is isomorphic to a subgroup of S_{n-1}.
    # If Aut(G) is cyclic, its size cannot exceed the maximum order of an element in S_{n-1}.
    max_order = landau_g(n - 1)
    automorphisms = []
    
    for target_gens in itertools.product(*valid_targets):
        mapping = [0] * n
        mapping[id_idx] = id_idx
        
        # Evaluate the mapping using the BFS spanning tree
        for curr, gen_pos, nxt in bfs_tree:
            mapping[nxt] = mult[mapping[curr]][target_gens[gen_pos]]
            
        # Check if the mapping is bijective
        visited_map = [False] * n
        is_bij = True
        for m in mapping:
            if visited_map[m]:
                is_bij = False
                break
            visited_map[m] = True
        if not is_bij:
            continue
            
        # Check if the mapping preserves multiplication with generators
        is_hom = True
        for i in range(n):
            mapped_i = mapping[i]
            for gen_pos, g_idx in enumerate(gens_idx):
                prod_idx = mult[i][g_idx]
                if mapping[prod_idx] != mult[mapped_i][target_gens[gen_pos]]:
                    is_hom = False
                    break
            if not is_hom:
                break
                
        if is_hom:
            automorphisms.append(Permutation(mapping))
            # Early abort if the automorphism group is too large to be cyclic
            if len(automorphisms) > max_order:
                return False
                
    aut_order = len(automorphisms)
    if aut_order == 0:
        return False
        
    # Check if the automorphism group is cyclic by finding a generator
    for p in automorphisms:
        if p.order() == aut_order:
            return True
            
    return False

def conditions(witness):
    try:
        h1 = is_aut_cyclic(witness)
    except Exception:
        h1 = False
        
    try:
        neg_q = not witness.is_abelian
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The automorphism group Aut(G) is a cyclic group",
    "¬Q: G is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1