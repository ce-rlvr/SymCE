import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Q8 = PermutationGroup(Permutation(0, 1, 2, 3)(4, 5, 6, 7), Permutation(0, 4, 2, 6)(1, 7, 3, 5))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, N = witness
        elif hasattr(witness, 'G') and hasattr(witness, 'N'):
            G = witness.G
            N = witness.N
        elif isinstance(witness, dict) and 'G' in witness and 'N' in witness:
            G = witness['G']
            N = witness['N']
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: Aut(G) is the automorphism group of G (Definition)
    h2 = True

    # H_3: Hol(G) is the semidirect product G \rtimes Aut(G) (Definition)
    h3 = True

    # ¬Q: N is not a normal subgroup of Hol(G)
    # In Hol(G) = G \rtimes Aut(G), a subgroup N of G is normal in Hol(G) 
    # if and only if N is a characteristic subgroup of G.
    try:
        if not h1:
            neg_q = False
        else:
            elements = list(G.generate())
            n = len(elements)
            elem_to_idx = {e: i for i, e in enumerate(elements)}
            
            if isinstance(N, PermutationGroup):
                N_elements = set(N.generate())
            else:
                N_elements = set(N)
                
            is_subset = all(e in elem_to_idx for e in N_elements)
            if not is_subset:
                neg_q = False
            else:
                id_elem = None
                for e in elements:
                    if e * e == e:
                        id_elem = e
                        break
                        
                has_id = id_elem in N_elements
                
                is_closed = True
                for a in N_elements:
                    for b in N_elements:
                        if a * b not in N_elements:
                            is_closed = False
                            break
                    if not is_closed:
                        break
                        
                has_inv = True
                for a in N_elements:
                    if a**-1 not in N_elements:
                        has_inv = False
                        break
                        
                is_subgroup = has_id and is_closed and has_inv
                
                if not is_subgroup:
                    neg_q = True
                else:
                    is_normal = True
                    for h in N_elements:
                        for g in elements:
                            if g * h * g**-1 not in N_elements:
                                is_normal = False
                                break
                        if not is_normal:
                            break
                            
                    if not is_normal:
                        neg_q = True
                    else:
                        id_idx = elem_to_idx[id_elem]
                        mult_table = [[0]*n for _ in range(n)]
                        for i in range(n):
                            for j in range(n):
                                mult_table[i][j] = elem_to_idx[elements[i] * elements[j]]
                                
                        gens = list(G.generators)
                        gen_indices = [elem_to_idx[g] for g in gens]
                        
                        def get_order(idx):
                            curr = idx
                            order = 1
                            while curr != id_idx:
                                curr = mult_table[curr][idx]
                                order += 1
                            return order
                            
                        gen_orders = [get_order(i) for i in gen_indices]
                        
                        possible_targets = []
                        for order in gen_orders:
                            targets = [i for i in range(n) if get_order(i) == order]
                            possible_targets.append(targets)
                            
                        is_characteristic = True
                        for target_tuple in itertools.product(*possible_targets):
                            mapping = {id_idx: id_idx}
                            valid = True
                            
                            queue = [(id_idx, id_idx)]
                            head = 0
                            while head < len(queue):
                                u, phi_u = queue[head]
                                head += 1
                                
                                for g_idx, t_idx in zip(gen_indices, target_tuple):
                                    v = mult_table[u][g_idx]
                                    phi_v = mult_table[phi_u][t_idx]
                                    
                                    if v in mapping:
                                        if mapping[v] != phi_v:
                                            valid = False
                                            break
                                    else:
                                        mapping[v] = phi_v
                                        queue.append((v, phi_v))
                                if not valid:
                                    break
                                    
                            if valid and len(mapping) == n and len(set(mapping.values())) == n:
                                for h in N_elements:
                                    h_idx = elem_to_idx[h]
                                    phi_h_idx = mapping[h_idx]
                                    if elements[phi_h_idx] not in N_elements:
                                        is_characteristic = False
                                        break
                            if not is_characteristic:
                                break
                                
                        neg_q = not is_characteristic
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Aut(G) is the automorphism group of G",
    "H_3: Hol(G) is the semidirect product G \\rtimes Aut(G), where Aut(G) acts on G by evaluation",
    "¬Q: N is not a normal subgroup of Hol(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3