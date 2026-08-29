import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.free_groups import FreeGroup, free_group
from sympy.combinatorics.fp_groups import FpGroup
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
    h1, h2, neg_q = False, False, False
    
    try:
        F = witness['F']
        X = witness['X']
        S = witness['S']
        R = witness['R']
        
        if isinstance(X, (list, tuple, set)):
            X_list = list(X)
        else:
            X_list = [X]
            
        if hasattr(S, 'group') and S.group == F:
            S_list = [S]
        else:
            S_list = list(S)
            
        if hasattr(R, 'group') and R.group == F:
            R_list = [R]
        else:
            R_list = list(R)
            
    except Exception:
        return [False, False, False]
        
    try:
        h1 = all(word.group == F for word in S_list) and list(F.generators) == X_list
    except Exception:
        h1 = False

    N_elements = set()
    identity = None
    try:
        G = witness['G']
        eval_map = witness['eval_map']
        N = witness['N']
        
        if hasattr(G, 'identity'):
            identity = G.identity
        elif eval_map:
            some_val = next(iter(eval_map.values()))
            identity = some_val**0 if hasattr(some_val, '__pow__') else some_val * some_val**-1
        else:
            identity = list(G)[0]**0
            
        if hasattr(G, 'generators'):
            G_gens = G.generators
        else:
            G_gens = G
            
        eval_S = []
        for word in S_list:
            res = identity
            for gen, power in word.array_form:
                mapped = eval_map.get(gen)
                if mapped is None and hasattr(gen, 'name'):
                    mapped = eval_map.get(gen.name)
                if mapped is None:
                    mapped = eval_map.get(str(gen))
                if mapped is None:
                    raise ValueError(f"Generator {gen} not found in eval_map")
                    
                if power > 0:
                    res = res * (mapped ** power)
                elif power < 0:
                    res = res * (mapped ** power)
            eval_S.append(res)
            
        nc_elements = set(eval_S)
        nc_elements.add(identity)
        queue = list(nc_elements)
        while queue:
            curr = queue.pop(0)
            for g in list(nc_elements):
                prod = curr * g
                if prod not in nc_elements:
                    nc_elements.add(prod)
                    queue.append(prod)
            for x in G_gens:
                conj = x**-1 * curr * x
                if conj not in nc_elements:
                    nc_elements.add(conj)
                    queue.append(conj)
                    
        if hasattr(N, 'generate'):
            N_elements = set(N.generate())
        elif hasattr(N, 'elements'):
            N_elements = set(N.elements)
        else:
            N_elements = set(N)
            N_elements.add(identity)
            queue = list(N_elements)
            while queue:
                curr = queue.pop(0)
                for g in list(N_elements):
                    prod = curr * g
                    if prod not in N_elements:
                        N_elements.add(prod)
                        queue.append(prod)
                        
        h2 = (nc_elements == N_elements)
    except Exception:
        h2 = False

    try:
        G = witness['G']
        
        if hasattr(G, 'order') and callable(G.order):
            G_order = G.order()
        elif hasattr(G, 'order'):
            G_order = G.order
        elif hasattr(G, 'generate'):
            G_order = len(list(G.generate()))
        else:
            if hasattr(G, 'generators'):
                G_gens = G.generators
            else:
                G_gens = G
            G_elements = set(G_gens)
            if identity is not None:
                G_elements.add(identity)
            queue = list(G_elements)
            while queue:
                curr = queue.pop(0)
                for g in list(G_elements):
                    prod = curr * g
                    if prod not in G_elements:
                        G_elements.add(prod)
                        queue.append(prod)
            G_order = len(G_elements)
            
        if not N_elements:
            if hasattr(witness['N'], 'generate'):
                N_elements = set(witness['N'].generate())
            elif hasattr(witness['N'], 'elements'):
                N_elements = set(witness['N'].elements)
            else:
                N_elements = set(witness['N'])
                if identity is not None:
                    N_elements.add(identity)
                
        order_GN = G_order / len(N_elements)
        
        fp_grp = FpGroup(F, R_list + S_list)
        
        try:
            order_fp = fp_grp.order()
        except Exception:
            order_fp = float('inf')
            
        neg_q = (order_GN != order_fp)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a set of words in the free group generated by X",
    "H_2: N is the normal closure in G of the subgroup generated by the images of the words in S under the canonical evaluation map",
    "¬Q: The quotient group G/N does NOT have the presentation <X | R ∪ S>"
]

N_HYP = 2
NEG_Q_INDEX = 2