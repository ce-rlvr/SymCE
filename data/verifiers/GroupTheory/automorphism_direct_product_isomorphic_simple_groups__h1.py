import math
import itertools
import functools
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import DirectProduct

# Top-level setup: named object bindings
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

def aut_group_size(G):
    """Computes the size of the automorphism group of a small PermutationGroup."""
    elements = list(G.generate())
    id_elem = G.identity
    if id_elem in elements:
        elements.remove(id_elem)
    elements = [id_elem] + elements
    
    n = len(elements)
    if n == 1: 
        return 1
    if n > 64:
        raise ValueError("Group too large for brute-force automorphism check")
        
    idx = {e: i for i, e in enumerate(elements)}
    table = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            table[i][j] = idx[elements[i] * elements[j]]
            
    # Precompute element orders to prune the search space
    orders = [0] * n
    for i in range(n):
        curr = i
        k = 1
        while curr != 0:
            curr = table[curr][i]
            k += 1
        orders[i] = k
        
    # Find a minimal generating set
    gens = []
    closure = {0}
    for i in range(1, n):
        if i not in closure:
            gens.append(i)
            new_closure = set(closure)
            added = True
            while added:
                added = False
                to_add = set()
                for x in new_closure:
                    for y in new_closure:
                        z = table[x][y]
                        if z not in new_closure and z not in to_add:
                            to_add.add(z)
                if to_add:
                    new_closure.update(to_add)
                    added = True
            closure = new_closure
            if len(closure) == n:
                break

    # Build a spanning tree of the Cayley graph to uniquely extend mappings
    tree_order = []
    tree_ops = {}
    closure = {0}
    queue = [0]
    
    while queue:
        curr = queue.pop(0)
        for g in gens:
            nxt = table[curr][g]
            if nxt not in closure:
                closure.add(nxt)
                tree_ops[nxt] = (curr, g)
                tree_order.append(nxt)
                queue.append(nxt)
                
            nxt2 = table[g][curr]
            if nxt2 not in closure:
                closure.add(nxt2)
                tree_ops[nxt2] = (g, curr)
                tree_order.append(nxt2)
                queue.append(nxt2)
                
    # Restrict targets for generators to elements of the same order
    valid_targets = []
    for g in gens:
        g_order = orders[g]
        targets = [i for i in range(n) if orders[i] == g_order]
        valid_targets.append(targets)
        
    ans = 0
    for target_gens in itertools.product(*valid_targets):
        mapping = {0: 0}
        for g, tg in zip(gens, target_gens):
            mapping[g] = tg
            
        # Extend mapping to all elements using the spanning tree
        for z in tree_order:
            x, y = tree_ops[z]
            mapping[z] = table[mapping[x]][mapping[y]]
            
        # An automorphism must be a bijection
        if len(set(mapping.values())) != n:
            continue
            
        # Verify it preserves the entire multiplication table
        full_valid = True
        for i in range(n):
            mi = mapping[i]
            for j in range(n):
                if mapping[table[i][j]] != table[mi][mapping[j]]:
                    full_valid = False
                    break
            if not full_valid:
                break
                
        if full_valid:
            ans += 1
            
    return ans

def conditions(witness):
    try:
        n, S, G = witness
    except Exception:
        return [False, False, False]
        
    # H_1: n is a positive integer
    try:
        n_int = int(n)
        h1 = (n_int == n) and (n_int > 0)
        n = n_int
    except Exception:
        h1 = False
        
    # H_2: G is the direct product of n copies of S
    try:
        if h1 and n < 10:
            expected_G = DirectProduct(*[S] * n)
            h2 = G.is_isomorphic(expected_G)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: Aut(G) is NOT isomorphic to the wreath product Aut(S) wr S_n
    try:
        if h1 and n < 10:
            aut_G_size = aut_group_size(G)
            aut_S_size = aut_group_size(S)
            wreath_size = (aut_S_size ** n) * math.factorial(n)
            # If sizes are different, they are definitely not isomorphic.
            neg_q = (aut_G_size != wreath_size)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is the direct product of n copies of S",
    "¬Q: Aut(G) is not isomorphic to the wreath product Aut(S) wr S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2