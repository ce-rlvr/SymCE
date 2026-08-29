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

def is_aut_group_cyclic(G):
    if getattr(G, 'is_trivial', False):
        return True
    
    try:
        elements = list(G.generate())
    except Exception:
        try:
            elements = list(G.elements)
        except Exception:
            return False
        
    n = len(elements)
    if n == 1:
        return True
        
    elem_idx = {e: i for i, e in enumerate(elements)}
    
    identity_idx = None
    for i in range(n):
        if elements[i] * elements[i] == elements[i]:
            identity_idx = i
            break
            
    if identity_idx is None:
        return False
        
    mult_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult_table[i][j] = elem_idx[elements[i] * elements[j]]
            
    orders = [1] * n
    for i in range(n):
        if i == identity_idx:
            continue
        curr = i
        order = 1
        while curr != identity_idx:
            curr = mult_table[curr][i]
            order += 1
        orders[i] = order
            
    try:
        gens = list(G.generators)
    except Exception:
        return False
        
    gen_indices = [elem_idx[g] for g in gens]
    gen_orders = [orders[g] for g in gen_indices]
    
    valid_images = []
    for g_ord in gen_orders:
        valid_images.append([i for i in range(n) if orders[i] == g_ord])
    
    automorphisms = []
    for img_tuple in itertools.product(*valid_images):
        mapping = {gen_indices[i]: img_tuple[i] for i in range(len(gen_indices))}
        closure = {identity_idx: identity_idx}
        for g, mg in mapping.items():
            closure[g] = mg
        
        queue = list(closure.keys())
        idx = 0
        valid = True
        while idx < len(queue):
            u = queue[idx]
            idx += 1
            for g in gen_indices:
                # u * g
                ug = mult_table[u][g]
                mu_mg = mult_table[closure[u]][closure[g]]
                if ug in closure:
                    if closure[ug] != mu_mg:
                        valid = False
                        break
                else:
                    closure[ug] = mu_mg
                    queue.append(ug)
                    
                # g * u
                gu = mult_table[g][u]
                mg_mu = mult_table[closure[g]][closure[u]]
                if gu in closure:
                    if closure[gu] != mg_mu:
                        valid = False
                        break
                else:
                    closure[gu] = mg_mu
                    queue.append(gu)
            if not valid:
                break
        
        if valid and len(closure) == n:
            if len(set(closure.values())) == n:
                aut = tuple(closure[i] for i in range(n))
                automorphisms.append(aut)
                
    aut_size = len(automorphisms)
    if aut_size <= 1:
        return True
        
    def compose(a, b):
        return tuple(a[b[i]] for i in range(n))
        
    for aut in automorphisms:
        order = 1
        curr = aut
        identity = tuple(range(n))
        while curr != identity:
            curr = compose(curr, aut)
            order += 1
        if order == aut_size:
            return True
            
    return False

def conditions(witness):
    try:
        h1 = bool(is_aut_group_cyclic(witness))
    except Exception:
        h1 = False
        
    try:
        neg_q = not bool(witness.is_abelian)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The automorphism group Aut(G) is a cyclic group",
    "¬Q: G is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1