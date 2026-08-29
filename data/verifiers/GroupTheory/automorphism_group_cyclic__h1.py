import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_order(G):
    o = G.order
    if callable(o):
        return o()
    return o

def get_automorphism_group(G):
    elements = list(G.generate())
    n = len(elements)
    if n == 1:
        return PermutationGroup([Permutation(0)])
        
    id_elem = None
    for e in elements:
        if e * e == e:
            id_elem = e
            break
            
    gens = G.generators
    
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    mult_table = [[elem_to_idx[x * y] for y in elements] for x in elements]
    
    def order(e):
        p = e
        k = 1
        while p != id_elem:
            p = p * e
            k += 1
        return k
        
    orders = [order(e) for e in elements]
    gen_indices = [elem_to_idx[g] for g in gens]
    
    possible_targets = []
    for g_idx in gen_indices:
        req_order = orders[g_idx]
        targets = [i for i, o in enumerate(orders) if o == req_order]
        possible_targets.append(targets)
        
    automorphisms = []
    id_idx = elem_to_idx[id_elem]
    for target_gen_indices in itertools.product(*possible_targets):
        mapping = {id_idx: id_idx}
        queue = [id_idx]
        
        is_valid = True
        head = 0
        while head < len(queue):
            x = queue[head]
            head += 1
            for i, g_idx in enumerate(gen_indices):
                y = mult_table[x][g_idx]
                mapped_y = mult_table[mapping[x]][target_gen_indices[i]]
                if y in mapping:
                    if mapping[y] != mapped_y:
                        is_valid = False
                        break
                else:
                    mapping[y] = mapped_y
                    queue.append(y)
            if not is_valid:
                break
                
        if is_valid and len(set(mapping.values())) == n:
            perm = [mapping[i] for i in range(n)]
            automorphisms.append(Permutation(perm))
            
    if not automorphisms:
        return PermutationGroup([Permutation(n-1)])
    return PermutationGroup(automorphisms)

def get_ZnZ_star_group(n):
    if n <= 1:
        return PermutationGroup([Permutation(0)])
    elements = [k for k in range(1, n) if math.gcd(k, n) == 1]
    k_to_idx = {k: i for i, k in enumerate(elements)}
    
    perms = []
    for a in elements:
        perm = []
        for x in elements:
            y = (a * x) % n
            perm.append(k_to_idx[y])
        perms.append(Permutation(perm))
        
    if not perms:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(perms)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, PermutationGroup):
            h1 = False
        else:
            n = get_order(witness)
            h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            n = int(get_order(witness))
            Aut_G = get_automorphism_group(witness)
            ZnZ_star = get_ZnZ_star_group(n)
            
            if get_order(Aut_G) != get_order(ZnZ_star):
                neg_q = True
            else:
                is_ab_Aut = Aut_G.is_abelian
                if callable(is_ab_Aut):
                    is_ab_Aut = is_ab_Aut()
                    
                is_ab_ZnZ = ZnZ_star.is_abelian
                if callable(is_ab_ZnZ):
                    is_ab_ZnZ = is_ab_ZnZ()
                    
                if is_ab_Aut != is_ab_ZnZ:
                    neg_q = True
                else:
                    def get_order_multiset(grp):
                        orders = []
                        elements = list(grp.generate())
                        id_elem = None
                        for e in elements:
                            if e * e == e:
                                id_elem = e
                                break
                        for e in elements:
                            p = e
                            k = 1
                            while p != id_elem:
                                p = p * e
                                k += 1
                            orders.append(k)
                        return sorted(orders)
                        
                    if get_order_multiset(Aut_G) != get_order_multiset(ZnZ_star):
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is a finite integer n",
    "¬Q: Aut(G) is not isomorphic to (Z/nZ)^x"
]

N_HYP = 1
NEG_Q_INDEX = 1