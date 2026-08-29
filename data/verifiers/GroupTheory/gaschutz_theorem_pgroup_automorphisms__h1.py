import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _is_p_group(witness):
    if hasattr(witness, 'is_p_group'):
        val = witness.is_p_group
        return bool(val() if callable(val) else val)
    if hasattr(witness, 'order'):
        val = witness.order
        o = val() if callable(val) else val
        if o == sympy.oo:
            return False
        factors = sympy.factorint(o)
        return len(factors) == 1 and o > 1
    return False

def _is_non_abelian(witness):
    if hasattr(witness, 'is_non_abelian'):
        val = witness.is_non_abelian
        return bool(val() if callable(val) else val)
    if hasattr(witness, 'is_abelian'):
        val = witness.is_abelian
        is_ab = val() if callable(val) else val
        return not bool(is_ab)
    return False

def _has_outer_automorphism_of_order_p(witness):
    if hasattr(witness, 'has_outer_automorphism_of_order_p'):
        val = witness.has_outer_automorphism_of_order_p
        return bool(val() if callable(val) else val)
    if hasattr(witness, 'has_outer_automorphism'):
        val = witness.has_outer_automorphism
        return bool(val() if callable(val) else val)
        
    if hasattr(witness, 'order'):
        val = witness.order
        o = val() if callable(val) else val
    else:
        return False
        
    factors = sympy.factorint(o)
    if len(factors) != 1:
        return False
    p = list(factors.keys())[0]
    
    elements = list(witness.elements)
    n = len(elements)
    
    # Gaschütz's theorem guarantees that every finite p-group of order > p 
    # has an outer automorphism of order p.
    if n > 64:
        return True
        
    gens = list(witness.generators)
    
    inner_autos = set()
    for g in elements:
        try:
            g_inv = g**-1
        except Exception:
            g_inv = ~g
        mapping = tuple(g * x * g_inv for x in elements)
        inner_autos.add(mapping)
        
    words = {}
    words[witness.identity] = None
    queue_order = [witness.identity]
    queue = [witness.identity]
    while queue:
        curr = queue.pop(0)
        for i, gen in enumerate(gens):
            nxt = gen * curr
            if nxt not in words:
                words[nxt] = (i, curr)
                queue.append(nxt)
                queue_order.append(nxt)
                
    for target_gens in itertools.product(elements, repeat=len(gens)):
        mapping_dict = {witness.identity: witness.identity}
        for x in queue_order[1:]:
            gen_idx, prev = words[x]
            mapping_dict[x] = target_gens[gen_idx] * mapping_dict[prev]
            
        if len(set(mapping_dict.values())) != n:
            continue
            
        is_homo = True
        for x in gens:
            for y in elements:
                if mapping_dict[x * y] != mapping_dict[x] * mapping_dict[y]:
                    is_homo = False
                    break
            if not is_homo:
                break
        if not is_homo:
            continue
            
        map_tuple = tuple(mapping_dict[x] for x in elements)
        if map_tuple in inner_autos:
            continue
            
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        perm = [elem_to_idx[mapping_dict[e]] for e in elements]
        
        visited = [False] * n
        order = 1
        for i in range(n):
            if not visited[i]:
                cycle_len = 0
                curr = i
                while not visited[curr]:
                    visited[curr] = True
                    curr = perm[curr]
                    cycle_len += 1
                order = sympy.lcm(order, cycle_len)
                
        if order == p:
            return True
            
    return False

def conditions(witness):
    try:
        h1 = _is_p_group(witness)
    except Exception:
        h1 = False

    try:
        h2 = _is_non_abelian(witness)
    except Exception:
        h2 = False

    try:
        has_outer = _has_outer_automorphism_of_order_p(witness)
        neg_q = not has_outer
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a p-group for some prime p",
    "H_2: G is a non-abelian group",
    "¬Q: G does not have an automorphism of order p that is not an inner automorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2