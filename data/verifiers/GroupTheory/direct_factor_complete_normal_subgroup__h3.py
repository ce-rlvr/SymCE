import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: Every automorphism of N is an inner automorphism",
    "¬Q: G is not isomorphic to the direct product N x C_G(N)"
]
N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = False
        if h1 and isinstance(N, PermutationGroup):
            is_sub = True
            G_elements = set(G.generate())
            for g in N.generators:
                if g not in G_elements:
                    is_sub = False
                    break
            if is_sub:
                N_elements = set(N.generate())
                is_normal = True
                for g in G.generators:
                    g_inv = g**-1
                    for n in N.generators:
                        if g * n * g_inv not in N_elements:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h2 = is_normal
    except Exception:
        h2 = False
        
    # H3: Every automorphism of N is an inner automorphism
    try:
        h3 = False
        if isinstance(N, PermutationGroup):
            gens = N.generators
            elements = list(N.generate())
            
            inner_autos = set()
            for n in elements:
                inner_autos.add(tuple((n * g * n**-1) for g in gens))
                
            elements_by_order = {}
            for e in elements:
                o = e.order()
                if o not in elements_by_order:
                    elements_by_order[o] = []
                elements_by_order[o].append(e)
                
            possible_images = []
            for g in gens:
                possible_images.append(elements_by_order.get(g.order(), []))
                
            all_inner = True
            for images in itertools.product(*possible_images):
                if images in inner_autos:
                    continue
                    
                mapping = {N.identity: N.identity}
                queue = [N.identity]
                valid = True
                while queue:
                    curr = queue.pop(0)
                    for g, h in zip(gens, images):
                        nxt = curr * g
                        nxt_img = mapping[curr] * h
                        if nxt in mapping:
                            if mapping[nxt] != nxt_img:
                                valid = False
                                break
                        else:
                            mapping[nxt] = nxt_img
                            queue.append(nxt)
                    if not valid:
                        break
                if valid and len(mapping) == len(elements) and len(set(mapping.values())) == len(elements):
                    all_inner = False
                    break
            h3 = all_inner
    except Exception:
        h3 = False
        
    # neg_Q: G is NOT isomorphic to N \times C_G(N)
    try:
        neg_q = False
        if h1 and isinstance(N, PermutationGroup):
            N_gens = N.generators
            C_elements = []
            for g in G.generate():
                if all(g * n == n * g for n in N_gens):
                    C_elements.append(g)
            if not C_elements:
                C = PermutationGroup([G.identity])
            else:
                C = PermutationGroup(C_elements)
                
            degN = N.degree
            degC = C.degree
            if degN == 0: degN = 1
            if degC == 0: degC = 1
            
            H_gens = []
            for g in N.generators:
                arr = [g(i) for i in range(degN)] + list(range(degN, degN + degC))
                H_gens.append(Permutation(arr))
            for g in C.generators:
                arr = list(range(degN)) + [g(i) + degN for i in range(degC)]
                H_gens.append(Permutation(arr))
                
            if not H_gens:
                H = PermutationGroup([Permutation([])])
            else:
                H = PermutationGroup(H_gens)
                
            if G.order() != H.order():
                neg_q = True
            elif G.is_abelian != H.is_abelian:
                neg_q = True
            else:
                def order_counts(grp):
                    counts = {}
                    for g in grp.generate():
                        o = g.order()
                        counts[o] = counts.get(o, 0) + 1
                    return counts
                if order_counts(G) != order_counts(H):
                    neg_q = True
                else:
                    try:
                        if hasattr(G, 'is_isomorphic'):
                            res = G.is_isomorphic(H)
                            if res is not None:
                                neg_q = not res
                    except Exception:
                        pass
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]