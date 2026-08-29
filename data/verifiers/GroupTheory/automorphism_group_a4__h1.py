import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def automorphism_group_is_S4(G):
    try:
        elements = list(G.elements)
        n = len(elements)
        if n == 1:
            return False
            
        identity = None
        for e in elements:
            if e * e == e:
                identity = e
                break
        if identity is None:
            return False
            
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        id_idx = elem_to_idx[identity]
        
        mult = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                mult[i][j] = elem_to_idx[elements[i] * elements[j]]
                
        gens = G.generators
        gen_indices = [elem_to_idx[g] for g in gens]
        
        orders = []
        for e in elements:
            curr = e
            o = 1
            while curr != identity:
                curr = curr * e
                o += 1
            orders.append(o)
            
        gen_orders = [orders[g] for g in gen_indices]
        
        valid_targets_per_gen = []
        for o in gen_orders:
            valid_targets = [i for i in range(n) if orders[i] == o]
            valid_targets_per_gen.append(valid_targets)
            
        automorphisms = []
        
        for target_gen_indices in itertools.product(*valid_targets_per_gen):
            mapping = {id_idx: id_idx}
            valid = True
            for g_idx, tg_idx in zip(gen_indices, target_gen_indices):
                if g_idx in mapping:
                    if mapping[g_idx] != tg_idx:
                        valid = False
                        break
                else:
                    mapping[g_idx] = tg_idx
                    
            if not valid:
                continue
                
            queue = list(mapping.keys())
            head = 0
            while head < len(queue):
                u = queue[head]
                head += 1
                for v in list(mapping.keys()):
                    # Check u * v
                    uv = mult[u][v]
                    mapped_uv = mult[mapping[u]][mapping[v]]
                    if uv in mapping:
                        if mapping[uv] != mapped_uv:
                            valid = False
                            break
                    else:
                        mapping[uv] = mapped_uv
                        queue.append(uv)
                        
                    # Check v * u
                    vu = mult[v][u]
                    mapped_vu = mult[mapping[v]][mapping[u]]
                    if vu in mapping:
                        if mapping[vu] != mapped_vu:
                            valid = False
                            break
                    else:
                        mapping[vu] = mapped_vu
                        queue.append(vu)
                if not valid:
                    break
                    
            if valid and len(mapping) == n and len(set(mapping.values())) == n:
                aut_tuple = tuple(mapping[i] for i in range(n))
                automorphisms.append(aut_tuple)
                
        if len(automorphisms) != 24:
            return False
            
        def compose(aut1, aut2):
            return tuple(aut1[aut2[i]] for i in range(n))
            
        aut_orders = []
        for aut in automorphisms:
            curr = aut
            order = 1
            id_aut = tuple(range(n))
            while curr != id_aut:
                curr = compose(curr, aut)
                order += 1
            aut_orders.append(order)
            
        order_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for o in aut_orders:
            if o in order_counts:
                order_counts[o] += 1
            else:
                return False
                
        # S4 has exactly 1 element of order 1, 9 of order 2, 8 of order 3, and 6 of order 4.
        if order_counts[1] == 1 and order_counts[2] == 9 and order_counts[3] == 8 and order_counts[4] == 6:
            return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if not hasattr(witness, 'elements') or not hasattr(witness, 'generators'):
            neg_q = False
        else:
            q_holds = automorphism_group_is_S4(witness)
            neg_q = not q_holds
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The automorphism group of G is not isomorphic to the symmetric group S4"
]

N_HYP = 0
NEG_Q_INDEX = 0