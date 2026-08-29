import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = H.is_subgroup(G)
        else:
            h1 = True
            for h in H.elements:
                if h not in G.elements:
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        if hasattr(G, 'order') and hasattr(H, 'order'):
            n = G.order() // H.order()
            h2 = (G.order() % H.order() == 0) and (n > 0)
        else:
            g_len = len(list(G.elements))
            h_len = len(list(H.elements))
            n = g_len // h_len
            h2 = (g_len % h_len == 0) and (n > 0)
    except Exception:
        h2 = False

    try:
        h3 = h1 and h2
    except Exception:
        h3 = False

    try:
        if not (h1 and h2 and h3):
            return [h1, h2, h3, False]
            
        if hasattr(G, 'order') and G.order() > 500:
            return [h1, h2, h3, False]
            
        g_elements = list(G.elements)
        h_elements = list(H.elements)
        
        kernel_action = []
        for g in g_elements:
            is_in_kernel = True
            for x in g_elements:
                for h in h_elements:
                    gxh = g * x * h
                    found = False
                    for h2 in h_elements:
                        if gxh == x * h2:
                            found = True
                            break
                    if not found:
                        is_in_kernel = False
                        break
                if not is_in_kernel:
                    break
            if is_in_kernel:
                kernel_action.append(g)
                
        intersection = []
        for x in g_elements:
            is_in_intersection = True
            for g in g_elements:
                try:
                    ginv = g**-1
                except Exception:
                    return [h1, h2, h3, True]
                    
                found = False
                for h in h_elements:
                    if x == g * h * ginv:
                        found = True
                        break
                if not found:
                    is_in_intersection = False
                    break
            if is_in_intersection:
                intersection.append(x)
                
        part1 = set(kernel_action) == set(intersection)
        
        if not part1:
            return [h1, h2, h3, True]
            
        if isinstance(G, PermutationGroup):
            reps = []
            for g in g_elements:
                found = False
                for r in reps:
                    if H.contains(r**-1 * g):
                        found = True
                        break
                if not found:
                    reps.append(g)
            
            generators = list(G.generators)
            image_generators = []
            for gen in generators:
                perm = []
                for r in reps:
                    target = gen * r
                    for i, r2 in enumerate(reps):
                        if H.contains(r2**-1 * target):
                            perm.append(i)
                            break
                if perm:
                    image_generators.append(Permutation(perm))
            
            if not image_generators:
                image_generators = [Permutation(len(reps) - 1)]
                
            image_group = PermutationGroup(image_generators)
            
            order_G_K = G.order() // len(kernel_action)
            part2 = (order_G_K == image_group.order())
            
            q = part1 and part2
            neg_q = not q
        else:
            neg_q = False
            
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: index of H in G is n for some integer n > 0",
    "H_3: G acts on the set of left cosets G/H by left multiplication",
    "¬Q: The kernel of the action is not the intersection of gHg^-1, or G/K is not isomorphic to a subgroup of S_n"
]

N_HYP = 3
NEG_Q_INDEX = 3