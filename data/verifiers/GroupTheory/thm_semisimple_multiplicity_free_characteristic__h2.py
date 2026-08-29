import math
import itertools
import functools
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    "H_1: G is a finite semisimple group",
    "H_2: N is a normal subgroup of G",
    "¬Q: N is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_order(grp):
    return grp.order() if callable(grp.order) else grp.order

def is_solvable(grp):
    return grp.is_solvable() if callable(grp.is_solvable) else grp.is_solvable

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
        
    H1 = False
    closures = []
    try:
        if isinstance(G, PermutationGroup) and 1 < get_order(G) <= 300000:
            checked = set()
            G_gens = G.generators
            
            # Compute all normal closures of elements. 
            # For a direct product of simple groups, this exactly yields all normal subgroups.
            for g in G.generate_dimino():
                if g in checked:
                    continue
                
                Q = [g]
                nc_gens = {g}
                while Q:
                    curr = Q.pop(0)
                    for gen in G_gens:
                        c1 = gen * curr * (~gen)
                        if c1 not in nc_gens:
                            nc_gens.add(c1)
                            Q.append(c1)
                        c2 = (~gen) * curr * gen
                        if c2 not in nc_gens:
                            nc_gens.add(c2)
                            Q.append(c2)
                
                NC = PermutationGroup(list(nc_gens))
                
                is_new = True
                for existing_NC in closures:
                    if get_order(NC) == get_order(existing_NC):
                        if all(NC.contains(gen) for gen in existing_NC.generators):
                            is_new = False
                            break
                
                if is_new:
                    closures.append(NC)
                    
                checked.update(nc_gens)
            
            # G is semisimple iff it has no non-trivial solvable normal subgroups
            H1 = True
            for NC in closures:
                if get_order(NC) > 1 and is_solvable(NC):
                    H1 = False
                    break
            
            # For finite groups, semisimple (direct product of non-abelian simple groups) 
            # also requires the group to be perfect.
            if H1:
                der = G.derived_subgroup()
                if get_order(der) != get_order(G):
                    H1 = False
    except Exception:
        H1 = False

    H2 = False
    try:
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            is_sub = True
            for gen in N.generators:
                if not G.contains(gen):
                    is_sub = False
                    break
            
            if is_sub:
                is_normal = True
                for n in N.generators:
                    for g in G.generators:
                        if not N.contains(g * n * (~g)):
                            is_normal = False
                            break
                    if not is_normal:
                        break
                H2 = is_normal
    except Exception:
        H2 = False

    neg_Q = False
    try:
        if H1 and H2:
            # In a finite semisimple group, a normal subgroup is characteristic 
            # if and only if it is the unique normal subgroup of its order.
            count = sum(1 for NC in closures if get_order(NC) == get_order(N))
            neg_Q = (count > 1)
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]