import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def is_simple(G):
    try:
        order = G.order()
        if order <= 1:
            return False
        # Fast path for groups of prime order < 100
        if order in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97):
            return True
            
        elements = list(G.generate())
        classes = []
        seen = set()
        for g in elements:
            if g in seen:
                continue
            cclass = set()
            for x in elements:
                conj = x * g * (x**-1)
                cclass.add(conj)
                seen.add(conj)
            classes.append(cclass)
            
        id_class = None
        for c in classes:
            if G.identity in c:
                id_class = c
                break
                
        other_classes = [c for c in classes if c != id_class]
        
        from itertools import combinations
        for r in range(1, len(other_classes)):
            for combo in combinations(other_classes, r):
                union_size = 1 + sum(len(c) for c in combo)
                if order % union_size == 0:
                    subset = set(id_class)
                    for c in combo:
                        subset.update(c)
                    
                    is_subgroup = True
                    subset_list = list(subset)
                    for x in subset_list:
                        for y in subset_list:
                            if x * y not in subset:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                    if is_subgroup:
                        return False
        return True
    except Exception:
        return False

def analyze_action(G, image_gens):
    try:
        if len(G.generators) != len(image_gens):
            return False, 0
        
        if not G.generators:
            return True, 1
            
        id_img = image_gens[0] ** -1 * image_gens[0]
        
        mapping = {G.identity: id_img}
        queue = [G.identity]
        gens = G.generators
        
        kernel_size = 0
        
        for g in queue:
            img_g = mapping[g]
            if img_g == id_img:
                kernel_size += 1
            for i, gen in enumerate(gens):
                nxt = g * gen
                nxt_img = img_g * image_gens[i]
                if nxt in mapping:
                    if mapping[nxt] != nxt_img:
                        return False, 0
                else:
                    mapping[nxt] = nxt_img
                    queue.append(nxt)
                    
        if len(mapping) != G.order():
            return False, 0
            
        return True, kernel_size
    except Exception:
        return False, 0

def conditions(witness):
    """
    witness: A tuple (G, image_gens) where:
      - G is a SymPy PermutationGroup.
      - image_gens is a list of Permutations (or other invertible objects) 
        representing the images of G.generators under the action homomorphism.
    """
    try:
        G, image_gens = witness
    except Exception:
        return [False, False, False]
        
    h1 = is_simple(G)
    
    valid_action, kernel_size = analyze_action(G, image_gens)
    h2 = valid_action
    
    neg_q = valid_action and kernel_size > 1
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a simple group",
    "H_2: G acts on a set X",
    "¬Q: The action of G on X is not faithful (kernel is not trivial)"
]

N_HYP = 2
NEG_Q_INDEX = 2