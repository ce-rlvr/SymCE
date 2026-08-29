import math
from itertools import product, permutations
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def expected_orders_Sn(S, n):
    S_orders = [e.order() for e in S.generate()]
    
    def lcm(a, b):
        return abs(a * b) // math.gcd(a, b)
        
    expected = []
    for tup in product(S_orders, repeat=n):
        res = 1
        for o in tup:
            res = lcm(res, o)
        expected.append(res)
    return sorted(expected)

def is_isomorphic_to_Sn(G, S, n):
    if G is None or S is None or n is None:
        return False
    try:
        if G.order() != S.order() ** n:
            return False
        if G.is_abelian != S.is_abelian:
            return False
        G_orders = sorted([e.order() for e in G.generate()])
        exp_orders = expected_orders_Sn(S, n)
        return G_orders == exp_orders
    except Exception:
        return False

def aut_group_size_fast(G):
    elements = list(G.generate())
    n_elems = len(elements)
    if n_elems == 1:
        return 1
    if n_elems > 100:
        raise ValueError("Group too large")
        
    idx = {e: i for i, e in enumerate(elements)}
    table = [[idx[e1 * e2] for e2 in elements] for e1 in elements]
    
    # Find a minimal generating set
    gens = []
    subgroup = {idx[G.identity]}
    for i in range(1, n_elems):
        if i not in subgroup:
            gens.append(i)
            queue = list(subgroup)
            head = 0
            while head < len(queue):
                curr = queue[head]
                head += 1
                for g in gens:
                    nxt = table[curr][g]
                    if nxt not in subgroup:
                        subgroup.add(nxt)
                        queue.append(nxt)
                    nxt = table[g][curr]
                    if nxt not in subgroup:
                        subgroup.add(nxt)
                        queue.append(nxt)
            if len(subgroup) == n_elems:
                break
                
    # Precompute orders
    orders = [1] * n_elems
    for i in range(n_elems):
        if i == idx[G.identity]:
            continue
        curr = i
        order = 1
        while curr != idx[G.identity]:
            curr = table[curr][i]
            order += 1
        orders[i] = order
        
    targets_per_gen = []
    for g in gens:
        o = orders[g]
        targets = [i for i in range(n_elems) if orders[i] == o]
        targets_per_gen.append(targets)
        
    count = 0
    for target_tuple in product(*targets_per_gen):
        # Check if targets generate G
        subgroup_t = {idx[G.identity]}
        queue_t = [idx[G.identity]]
        head_t = 0
        while head_t < len(queue_t):
            curr = queue_t[head_t]
            head_t += 1
            for t in target_tuple:
                nxt = table[curr][t]
                if nxt not in subgroup_t:
                    subgroup_t.add(nxt)
                    queue_t.append(nxt)
        if len(subgroup_t) < n_elems:
            continue
            
        # Check if it extends to a homomorphism
        mapping = {idx[G.identity]: idx[G.identity]}
        valid = True
        queue_m = [(idx[G.identity], idx[G.identity])]
        
        head_m = 0
        while head_m < len(queue_m) and valid:
            x, tx = queue_m[head_m]
            head_m += 1
            
            for g, tg in zip(gens, target_tuple):
                y = table[x][g]
                ty = table[tx][tg]
                if y in mapping:
                    if mapping[y] != ty:
                        valid = False
                        break
                else:
                    mapping[y] = ty
                    queue_m.append((y, ty))
                    
        if valid and len(mapping) == n_elems:
            is_hom = True
            for i in range(n_elems):
                mi = mapping[i]
                for j in range(n_elems):
                    if mapping[table[i][j]] != table[mi][mapping[j]]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            if is_hom:
                count += 1
                
    return count

def conditions(witness):
    try:
        if isinstance(witness, dict):
            S = witness.get('S')
            n = witness.get('n')
            G = witness.get('G')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                S, n, G = witness
            elif len(witness) == 2:
                S, n = witness
                try:
                    from sympy.combinatorics import DirectProduct
                    G = DirectProduct(*[S]*n)
                except Exception:
                    G = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: n is a positive integer
    try:
        h1 = type(n) is int and n > 0
    except Exception:
        h1 = False
        
    # H2: G is the direct product of n copies of S
    try:
        h2 = is_isomorphic_to_Sn(G, S, n)
    except Exception:
        h2 = False
        
    # neg_Q: Aut(G) is NOT isomorphic to Aut(S) wr S_n
    try:
        size_aut_G = aut_group_size_fast(G)
        size_aut_S = aut_group_size_fast(S)
        size_wreath = (size_aut_S ** n) * math.factorial(n)
        
        neg_q = (size_aut_G != size_wreath)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is the direct product of n copies of S",
    "¬Q: Aut(G) is not isomorphic to Aut(S) wr S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2