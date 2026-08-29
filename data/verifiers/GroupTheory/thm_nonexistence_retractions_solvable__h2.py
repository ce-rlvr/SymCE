import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_semisimple(G):
    if not isinstance(G, PermutationGroup):
        return False
    if G.order() == 1:
        return True
    
    elements = list(G.generate())
    for g in elements:
        if getattr(g, 'is_Identity', False) or g == G.identity:
            continue
        
        # Find the normal closure of g
        closure_gens = {g}
        queue = [g]
        while queue:
            curr = queue.pop(0)
            for gen in G.generators:
                conj = gen * curr * ~gen
                if conj not in closure_gens:
                    closure_gens.add(conj)
                    queue.append(conj)
        
        # Check if closure_gens commute with each other
        closure_gens_list = list(closure_gens)
        is_abelian = True
        for i in range(len(closure_gens_list)):
            for j in range(i + 1, len(closure_gens_list)):
                if closure_gens_list[i] * closure_gens_list[j] != closure_gens_list[j] * closure_gens_list[i]:
                    is_abelian = False
                    break
            if not is_abelian:
                break
        
        if is_abelian:
            # Found a non-trivial abelian normal subgroup
            return False
            
    return True

def is_retraction(G, S, r):
    if not isinstance(S, PermutationGroup):
        return False
    
    G_elements = set(G.generate())
    for gen in S.generators:
        if gen not in G_elements:
            return False
            
    S_elements = set(S.generate())
    
    for s in S_elements:
        rs = r(s) if callable(r) else r.get(s)
        if rs != s:
            return False
            
    for g1 in G_elements:
        rg1 = r(g1) if callable(r) else r.get(g1)
        if rg1 not in S_elements:
            return False
        for g2 in G_elements:
            rg2 = r(g2) if callable(r) else r.get(g2)
            if rg2 not in S_elements:
                return False
            g1g2 = g1 * g2
            rg1g2 = r(g1g2) if callable(r) else r.get(g1g2)
            if rg1g2 != rg1 * rg2:
                return False
                
    return True

def conditions(witness):
    try:
        G, S, r = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_semisimple(G)
    except Exception:
        h1 = False
        
    try:
        h2 = is_retraction(G, S, r)
    except Exception:
        h2 = False
        
    try:
        nq = S.order() > 1
    except Exception:
        nq = False
        
    return [h1, h2, nq]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: r: G \\to S is a group homomorphism such that r(s) = s for all s \\in S",
    "¬Q: S is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2