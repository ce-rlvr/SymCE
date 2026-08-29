import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_holomorph(G):
    elements = list(G.generate())
    n = len(elements)
    if n == 1:
        return PermutationGroup([Permutation(0)])
        
    mult = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult[i][j] = elements.index(elements[i] * elements[j])
            
    ident = None
    for i in range(n):
        if all(mult[i][j] == j for j in range(n)):
            ident = i
            break

    gen_indices = []
    for g in G.generators:
        idx = elements.index(g)
        if idx != ident and idx not in gen_indices:
            gen_indices.append(idx)
            
    if not gen_indices:
        return PermutationGroup([Permutation(0)])

    bfs_order = [ident]
    visited = {ident}
    parent = {} 
    
    queue = [ident]
    while queue:
        curr = queue.pop(0)
        for g_idx in gen_indices:
            nxt = mult[curr][g_idx]
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = (curr, g_idx)
                bfs_order.append(nxt)
                queue.append(nxt)
                
    auts = []
    for target_tuple in itertools.product(range(n), repeat=len(gen_indices)):
        gen_map = dict(zip(gen_indices, target_tuple))
        
        mapping = {ident: ident}
        valid = True
        for i in bfs_order:
            if i == ident:
                continue
            j, k = parent[i]
            mapped_j = mapping[j]
            mapped_k = gen_map[k]
            mapped_i = mult[mapped_j][mapped_k]
            
            if i in gen_map:
                if mapped_i != gen_map[i]:
                    valid = False
                    break
            mapping[i] = mapped_i
            
        if not valid:
            continue
            
        if len(set(mapping.values())) != n:
            continue
            
        is_hom = True
        for x in range(n):
            for y in range(n):
                if mapping[mult[x][y]] != mult[mapping[x]][mapping[y]]:
                    is_hom = False
                    break
            if not is_hom:
                break
                
        if is_hom:
            p = [mapping[i] for i in range(n)]
            auts.append(p)
            
    lambda_gens = []
    for i in range(n):
        p = [mult[i][j] for j in range(n)]
        lambda_gens.append(Permutation(p))
        
    aut_gens = [Permutation(p) for p in auts]
    
    return PermutationGroup(lambda_gens + aut_gens)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
        elif isinstance(witness, (tuple, list)) and len(witness) >= 2:
            G = witness[0]
            N = witness[-1]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: Sym(G) is the symmetric group on the underlying set of G
    h2 = True

    # H3: lambda is the left regular representation
    h3 = True

    # neg_Q: N is not isomorphic to the holomorph of G
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        elif not isinstance(N, PermutationGroup):
            neg_q = True
        else:
            hol_G = get_holomorph(G)
            neg_q = not N.is_isomorphic(hol_G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Sym(G) is the symmetric group on the underlying set of G",
    "H_3: lambda is the left regular representation",
    "¬Q: N is not isomorphic to the holomorph of G"
]

N_HYP = 3
NEG_Q_INDEX = 3