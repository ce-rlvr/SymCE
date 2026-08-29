import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import factorint

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
V4 = PermutationGroup([
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
])

def count_automorphisms(G):
    elements = list(G.generate())
    n_el = len(elements)
    if n_el > 64:
        return None
    
    idx = {e: i for i, e in enumerate(elements)}
    mult = [[idx[e1 * e2] for e2 in elements] for e1 in elements]
    
    id_idx = None
    for i in range(n_el):
        if mult[i][i] == i:
            id_idx = i
            break
            
    gens = []
    subgroup = {id_idx}
    for i in range(n_el):
        if i not in subgroup:
            gens.append(i)
            new_subgroup = set(subgroup)
            queue = [i]
            while queue:
                curr = queue.pop(0)
                new_subgroup.add(curr)
                for x in list(new_subgroup):
                    y = mult[curr][x]
                    if y not in new_subgroup:
                        new_subgroup.add(y)
                        queue.append(y)
                    y = mult[x][curr]
                    if y not in new_subgroup:
                        new_subgroup.add(y)
                        queue.append(y)
            subgroup = new_subgroup
            if len(subgroup) == n_el:
                break
                
    def get_order(x):
        curr = x
        ord = 1
        while curr != id_idx:
            curr = mult[curr][x]
            ord += 1
        return ord

    orders = [get_order(i) for i in range(n_el)]
    
    valid_auts = 0
    
    def search(gen_idx, current_mapping):
        nonlocal valid_auts
        if gen_idx == len(gens):
            if len(current_mapping) == n_el:
                valid_auts += 1
            return
        
        g = gens[gen_idx]
        for target in range(n_el):
            if orders[target] != orders[g]:
                continue
            
            new_mapping = current_mapping.copy()
            new_mapping[g] = target
            
            queue = [(g, target)]
            consistent = True
            while queue and consistent:
                x, fx = queue.pop(0)
                mapped_items = list(new_mapping.items())
                for y, fy in mapped_items:
                    xy = mult[x][y]
                    fxy = mult[fx][fy]
                    if xy in new_mapping:
                        if new_mapping[xy] != fxy:
                            consistent = False
                            break
                    else:
                        new_mapping[xy] = fxy
                        queue.append((xy, fxy))
                        
                    yx = mult[y][x]
                    fyx = mult[fy][fx]
                    if yx in new_mapping:
                        if new_mapping[yx] != fyx:
                            consistent = False
                            break
                    else:
                        new_mapping[yx] = fyx
                        queue.append((yx, fyx))
            
            if consistent:
                if len(set(new_mapping.values())) == len(new_mapping):
                    search(gen_idx + 1, new_mapping)

    search(0, {id_idx: id_idx})
    return valid_auts

def conditions(witness) -> list[bool]:
    try:
        p, n, G = witness
    except Exception:
        return [False, False, False]
        
    # H1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False
        
    # H2: G is an elementary abelian p-group of order p^n
    try:
        if not getattr(G, 'is_abelian', False):
            h2 = False
        else:
            elements = list(G.generate())
            if len(elements) != p**n:
                h2 = False
            else:
                id_elem = None
                for x in elements:
                    if x * x == x:
                        id_elem = x
                        break
                
                h2 = True
                for x in elements:
                    if (x**p) != id_elem:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    # neg_Q: Aut(G) is not isomorphic to GL(n, p)
    try:
        aut_order = count_automorphisms(G)
        if aut_order is None:
            neg_q = False
        else:
            # Order of GL(n, p) assuming p is a prime (field formula)
            gl_order = 1
            for i in range(n):
                gl_order *= (p**n - p**i)
                
            # Order of GL(n, Z/pZ) assuming p is composite (ring formula)
            try:
                if p <= 1:
                    gl_ring = gl_order
                else:
                    factors = factorint(p)
                    gl_ring = 1
                    for q, k in factors.items():
                        term = q**(n**2 * (k - 1))
                        for i in range(n):
                            term *= (q**n - q**i)
                        gl_ring *= term
            except Exception:
                gl_ring = gl_order
                
            # If the automorphism group order matches neither plausible interpretation 
            # of GL(n, p), they are definitively not isomorphic.
            neg_q = (aut_order != gl_order) and (aut_order != gl_ring)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is an elementary abelian p-group of order p^n",
    "¬Q: Aut(G) is not isomorphic to GL(n, p)"
]

N_HYP = 2
NEG_Q_INDEX = 2