import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
from itertools import product

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_semisimple(G):
    """
    A finite group is semisimple (in the sense of direct product of simple groups)
    if it is a direct product of simple groups.
    """
    try:
        if G.order() == 1:
            return True
    except Exception:
        pass
        
    try:
        if G.is_simple():
            return True
    except Exception:
        pass
        
    try:
        if G.is_abelian:
            for g in G.elements:
                if g.order() == 1:
                    continue
                factors = factorint(g.order())
                if any(v > 1 for v in factors.values()):
                    return False
            return True
    except Exception:
        pass
        
    try:
        normals = G.normal_subgroups()
        for N in normals:
            has_comp = False
            for M in normals:
                if N.intersect(M).order() == 1 and N.order() * M.order() == G.order():
                    has_comp = True
                    break
            if not has_comp:
                return False
        return True
    except Exception:
        pass
        
    return False

def is_F_G_trivial(G):
    """
    The center of Hol(G) is isomorphic to F(G), the subgroup of elements in G
    fixed by all automorphisms of G. This function returns True if F(G) is trivial.
    """
    try:
        elements = list(G.elements)
        n = len(elements)
        if n == 1:
            return True
            
        gens = G.generators
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        mult_table = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                mult_table[i][j] = elem_to_idx[elements[i] * elements[j]]
                
        words = {elem_to_idx[G.identity]: []}
        queue = [elem_to_idx[G.identity]]
        gen_list = list(gens)
        
        while queue:
            curr = queue.pop(0)
            for i, g in enumerate(gen_list):
                nxt = elem_to_idx[elements[curr] * g]
                if nxt not in words:
                    words[nxt] = words[curr] + [i]
                    queue.append(nxt)
                    
        orders = [0] * n
        for i in range(n):
            curr = i
            k = 1
            while curr != elem_to_idx[G.identity]:
                curr = mult_table[curr][i]
                k += 1
            orders[i] = k
            
        gen_orders = [orders[elem_to_idx[g]] for g in gen_list]
        
        valid_images_per_gen = []
        for go in gen_orders:
            valid_images = [i for i in range(n) if orders[i] == go]
            valid_images_per_gen.append(valid_images)
            
        fixed_indices = set(range(n))
        
        for img_tuple in product(*valid_images_per_gen):
            mapping = [0] * n
            for i in range(n):
                val = elem_to_idx[G.identity]
                for gen_idx in words[i]:
                    val = mult_table[val][img_tuple[gen_idx]]
                mapping[i] = val
                
            if len(set(mapping)) != n:
                continue
                
            is_hom = True
            for i in range(n):
                for j in range(n):
                    if mapping[mult_table[i][j]] != mult_table[mapping[i]][mapping[j]]:
                        is_hom = False
                        break
                if not is_hom:
                    break
                    
            if is_hom:
                new_fixed = set()
                for idx in fixed_indices:
                    if mapping[idx] == idx:
                        new_fixed.add(idx)
                fixed_indices = new_fixed
                
                if len(fixed_indices) == 1:
                    return True
                    
        return len(fixed_indices) == 1
    except Exception:
        return None

def conditions(witness):
    try:
        if not hasattr(witness, 'elements') or not hasattr(witness, 'order'):
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: G is a semisimple group
    try:
        h1 = is_semisimple(witness)
    except Exception:
        h1 = False
        
    # H_2: G is a non-trivial group
    try:
        h2 = witness.order() > 1
    except Exception:
        h2 = False
        
    # neg_Q: The center of Hol(G) is not the trivial subgroup
    try:
        f_trivial = is_F_G_trivial(witness)
        if f_trivial is None:
            neg_q = False
        else:
            neg_q = not f_trivial
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "H_2: G is a non-trivial group",
    "¬Q: The center of Hol(G) is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2