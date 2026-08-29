import math
import itertools
from sympy.combinatorics import Permutation, PermutationGroup
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

# Define the quaternion group Q8 explicitly
Q8 = PermutationGroup(
    Permutation(0, 2, 1, 3)(4, 7, 5, 6),
    Permutation(0, 4, 1, 5)(2, 6, 3, 7)
)

def is_isomorphic_to_Q8(G):
    try:
        if not getattr(G, 'is_group', False) and not hasattr(G, 'generators'):
            return False
        if G.order() != 8:
            return False
        if G.is_abelian:
            return False
        elements = list(G.elements)
        # Q8 is the unique non-abelian group of order 8 with exactly one element of order 2
        order_2_count = sum(1 for g in elements if g.order() == 2)
        return order_2_count == 1
    except Exception:
        return False

def is_automorphism_group_NOT_S4(G):
    try:
        if not getattr(G, 'is_group', False) and not hasattr(G, 'generators'):
            return True
            
        if hasattr(G, 'order'):
            if G.order() > 64:
                return True
                
        elements = list(G.elements)
        gens = list(G.generators)
        
        orders = {e: e.order() for e in elements}
        gen_orders = [orders[g] for g in gens]
        
        candidates = []
        for o in gen_orders:
            candidates.append([e for e in elements if orders[e] == o])
            
        candidates_count = 1
        for c in candidates:
            candidates_count *= len(c)
            
        if candidates_count > 100000:
            return True
            
        autos = []
        for p in itertools.product(*candidates):
            mapping = {G.identity: G.identity}
            valid = True
            queue = [G.identity]
            
            while queue:
                curr = queue.pop(0)
                curr_target = mapping[curr]
                for g, g_target in zip(gens, p):
                    nxt = curr * g
                    nxt_target = curr_target * g_target
                    if nxt in mapping:
                        if mapping[nxt] != nxt_target:
                            valid = False
                            break
                    else:
                        mapping[nxt] = nxt_target
                        queue.append(nxt)
                if not valid:
                    break
                    
            if valid and len(mapping) == len(elements) and len(set(mapping.values())) == len(elements):
                autos.append(mapping)
                
        if len(autos) != 24:
            return True
            
        # S4 is the unique group of order 24 with no elements of order > 4
        for mapping in autos:
            visited = set()
            order = 1
            for e in elements:
                if e not in visited:
                    curr = e
                    cycle_len = 0
                    while curr not in visited:
                        visited.add(curr)
                        curr = mapping[curr]
                        cycle_len += 1
                    if order != 0 and cycle_len != 0:
                        order = abs(order * cycle_len) // math.gcd(order, cycle_len)
            if order not in (1, 2, 3, 4):
                return True
                
        return False
    except Exception:
        return True

def conditions(witness) -> list[bool]:
    h1 = is_isomorphic_to_Q8(witness)
    neg_q = is_automorphism_group_NOT_S4(witness)
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is isomorphic to the quaternion group of order 8",
    "¬Q: The automorphism group of G is NOT isomorphic to the symmetric group S_4"
]

N_HYP = 1
NEG_Q_INDEX = 1