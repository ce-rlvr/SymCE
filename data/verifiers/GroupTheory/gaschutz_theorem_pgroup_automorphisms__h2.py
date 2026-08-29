import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import itertools
import math

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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            G = witness[0]
            p_val = witness[1] if len(witness) > 1 else None
        else:
            G = witness
            p_val = None
    except Exception:
        return [False, False, False]

    # H1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup) and G.order() < float('inf')
    except Exception:
        h1_ok = False

    # H2: G is a non-abelian group
    try:
        h2_ok = not G.is_abelian
    except Exception:
        h2_ok = False

    # neg_Q: G does not have an automorphism of order p that is not an inner automorphism
    try:
        if not isinstance(G, PermutationGroup) or G.order() > 200:
            neg_q_ok = False
        else:
            elements = list(G.generate())
            n = len(elements)
            elem_to_idx = {e: i for i, e in enumerate(elements)}
            mul = [[0]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    mul[i][j] = elem_to_idx[elements[i] * elements[j]]
                    
            inner_autos = set()
            for g in elements:
                g_inv = g**-1
                mapping = tuple(elem_to_idx[g * x * g_inv] for x in elements)
                inner_autos.add(mapping)
                
            gens = G.generators
            gen_indices = [elem_to_idx[g] for g in gens]
            
            words = {elem_to_idx[G.identity]: []}
            queue = [elem_to_idx[G.identity]]
            while queue:
                curr = queue.pop(0)
                for i, g_idx in enumerate(gen_indices):
                    nxt = mul[curr][g_idx]
                    if nxt not in words:
                        words[nxt] = words[curr] + [i]
                        queue.append(nxt)
                        
            def get_mapping(gen_images):
                mapping = [-1] * n
                for i in range(n):
                    curr = elem_to_idx[G.identity]
                    for gen_idx in words[i]:
                        curr = mul[curr][gen_images[gen_idx]]
                    mapping[i] = curr
                return tuple(mapping)
                
            gen_orders = [g.order() for g in gens]
            elem_orders = [e.order() for e in elements]
            
            autos = []
            for gen_images in itertools.product(range(n), repeat=len(gens)):
                valid = True
                for i in range(len(gens)):
                    if elem_orders[gen_images[i]] != gen_orders[i]:
                        valid = False
                        break
                if not valid:
                    continue
                    
                mapping = get_mapping(gen_images)
                if len(set(mapping)) != n:
                    continue
                is_homo = True
                for i in range(n):
                    for j in range(n):
                        if mapping[mul[i][j]] != mul[mapping[i]][mapping[j]]:
                            is_homo = False
                            break
                    if not is_homo:
                        break
                if is_homo:
                    autos.append(mapping)
                    
            def get_order(mapping, n):
                visited = [False] * n
                order = 1
                for i in range(n):
                    if not visited[i]:
                        length = 0
                        curr = i
                        while not visited[curr]:
                            visited[curr] = True
                            curr = mapping[curr]
                            length += 1
                        order = (order * length) // math.gcd(order, length)
                return order

            has_outer_auto = False
            if p_val is not None:
                for mapping in autos:
                    if mapping not in inner_autos and get_order(mapping, n) == p_val:
                        has_outer_auto = True
                        break
            else:
                for mapping in autos:
                    if mapping not in inner_autos:
                        ord_m = get_order(mapping, n)
                        if isprime(ord_m):
                            has_outer_auto = True
                            break
                            
            neg_q_ok = not has_outer_auto
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a non-abelian group",
    "¬Q: G does not have an automorphism of order p that is not an inner automorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2