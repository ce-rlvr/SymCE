import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
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
    if hasattr(G, 'is_simple'):
        res = G.is_simple
        if res is not None:
            if callable(res):
                return res()
            return res
            
    order = G.order()
    if order <= 1:
        return False
    if order in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97):
        return True
        
    if hasattr(G, 'center'):
        try:
            C = G.center()
            if C.order() > 1 and C.order() < order:
                return False
        except Exception:
            pass
            
    count = 0
    try:
        elements = G.generate(method='dimino')
    except Exception:
        elements = G.elements
        
    for g in elements:
        if g.is_Identity:
            continue
        count += 1
        if count > 200:
            break
            
        closure_gens = [g]
        G_gens = list(G.generators)
        current_group = PermutationGroup(closure_gens)
        while True:
            ord_c = current_group.order()
            new_gens = list(current_group.generators)
            for gen in G_gens:
                for h in current_group.generators:
                    new_gens.append(~gen * h * gen)
                    new_gens.append(gen * h * ~gen)
            current_group = PermutationGroup(new_gens)
            if current_group.order() == ord_c:
                break
        if current_group.order() < order:
            return False
            
    return True

def conditions(witness):
    try:
        G, A = witness
    except Exception:
        return [False, False, False, False, False]
        
    # H1: G is a perfect group
    try:
        h1 = (G.derived_subgroup().order() == G.order())
    except Exception:
        h1 = False
        
    # H2: X is a non-empty set
    try:
        h2 = (G.degree > 0)
    except Exception:
        h2 = False
        
    # H3: G acts faithfully and primitively on X
    try:
        h3 = bool(G.is_primitive())
    except Exception:
        h3 = False
        
    # H4: The conjugates of A in G generate the group G
    try:
        if hasattr(A, 'generators'):
            A_gens = list(A.generators)
        elif isinstance(A, Permutation):
            A_gens = [A]
        else:
            A_gens = list(A)
            
        if not A_gens:
            h4 = (G.order() == 1)
        else:
            closure_gens = list(A_gens)
            G_gens = list(G.generators)
            current_group = PermutationGroup(closure_gens)
            while True:
                ord_c = current_group.order()
                new_gens = list(current_group.generators)
                for gen in G_gens:
                    for h in current_group.generators:
                        new_gens.append(~gen * h * gen)
                        new_gens.append(gen * h * ~gen)
                current_group = PermutationGroup(new_gens)
                if current_group.order() == ord_c:
                    break
            h4 = (current_group.order() == G.order())
    except Exception:
        h4 = False
        
    # neg_Q: G is not a simple group
    try:
        neg_q = not is_simple(G)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a perfect group",
    "H_2: X is a non-empty set",
    "H_3: G acts faithfully and primitively on X",
    "H_4: The conjugates of A in G generate the group G",
    "¬Q: G is not a simple group"
]

N_HYP = 4
NEG_Q_INDEX = 4