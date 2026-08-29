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
        # Check if witness is a valid group-like object with generators
        if not hasattr(witness, 'generators'):
            return [False, False]
            
        # H_1: The center of G is the trivial subgroup
        try:
            C = witness.center()
            h1 = (C.order() == 1)
        except Exception:
            h1 = False
            
        # neg_Q: The center of the automorphism group of G is not the trivial subgroup
        try:
            elements = list(witness.generate())
            n = len(elements)
            if n <= 1:
                neg_q = False
            else:
                elem_to_idx = {e: i for i, e in enumerate(elements)}
                mul_table = [[0] * n for _ in range(n)]
                for i in range(n):
                    for j in range(n):
                        mul_table[i][j] = elem_to_idx[elements[i] * elements[j]]
                        
                id_elem = None
                for e in elements:
                    if e * e == e:
                        id_elem = e
                        break
                id_idx = elem_to_idx[id_elem]
                
                gens_idx = [elem_to_idx[g] for g in witness.generators]
                orders = [elements[i].order() for i in range(n)]
                
                gen_possible_images = []
                for g_idx in gens_idx:
                    o = orders[g_idx]
                    gen_possible_images.append([i for i in range(n) if orders[i] == o])
                    
                auts = []
                for gen_images in itertools.product(*gen_possible_images):
                    mapping = {id_idx: id_idx}
                    possible = True
                    for g_idx, img_idx in zip(gens_idx, gen_images):
                        if g_idx in mapping:
                            if mapping[g_idx] != img_idx:
                                possible = False
                                break
                        else:
                            mapping[g_idx] = img_idx
                    if not possible:
                        continue
                        
                    frontier = list(mapping.keys())
                    while frontier and possible:
                        new_frontier = []
                        for x in frontier:
                            for g_idx in gens_idx:
                                y = mul_table[x][g_idx]
                                expected_img = mul_table[mapping[x]][mapping[g_idx]]
                                if y not in mapping:
                                    mapping[y] = expected_img
                                    new_frontier.append(y)
                                else:
                                    if mapping[y] != expected_img:
                                        possible = False
                                        break
                            if not possible:
                                break
                        frontier = new_frontier
                        
                    if possible and len(mapping) == n and len(set(mapping.values())) == n:
                        auts.append([mapping[i] for i in range(n)])
                        
                center_size = 0
                for f in auts:
                    is_center = True
                    for g in auts:
                        for i in range(n):
                            if f[g[i]] != g[f[i]]:
                                is_center = False
                                break
                        if not is_center:
                            break
                    if is_center:
                        center_size += 1
                        
                neg_q = (center_size > 1)
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: The center of G is the trivial subgroup",
    "¬Q: The center of the automorphism group of G is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1