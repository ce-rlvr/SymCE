import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def is_identity(g):
    return len(g.support()) == 0

def get_conjugacy_class(G, g):
    gens = G.generators
    orbit = [g]
    orbit_set = {g}
    for curr in orbit:
        for gen in gens:
            conj = ~gen * curr * gen
            if conj not in orbit_set:
                orbit_set.add(conj)
                orbit.append(conj)
    return orbit

def get_all_conjugacy_classes(G):
    classes = []
    seen = set()
    count = 0
    for g in G.generate():
        count += 1
        if count > 20000:
            raise ValueError("Group too large")
        if g in seen:
            continue
        orbit = get_conjugacy_class(G, g)
        classes.append(orbit)
        seen.update(orbit)
    return classes

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    if not h1:
        return [False, False, False]

    try:
        classes = get_all_conjugacy_classes(witness)
    except Exception:
        return [True, False, False]

    try:
        if witness.order() == 1:
            h2 = True
        else:
            h2 = True
            for orbit in classes:
                if is_identity(orbit[0]):
                    continue
                is_abelian = True
                for i in range(len(orbit)):
                    for j in range(i + 1, len(orbit)):
                        if orbit[i] * orbit[j] != orbit[j] * orbit[i]:
                            is_abelian = False
                            break
                    if not is_abelian:
                        break
                if is_abelian:
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        if witness.order() == 1:
            neg_q = False
        else:
            if not h2:
                # If it has an abelian normal subgroup, it cannot be a direct product of non-abelian simple groups
                neg_q = True
            else:
                N_groups = []
                for orbit in classes:
                    if is_identity(orbit[0]):
                        N_groups.append(None)
                    else:
                        N_groups.append(PermutationGroup(orbit))
                        
                minimal_N = []
                for i in range(len(classes)):
                    if is_identity(classes[i][0]):
                        continue
                    is_minimal = True
                    for j in range(len(classes)):
                        if i == j or is_identity(classes[j][0]):
                            continue
                        if classes[j][0] in N_groups[i]:
                            if classes[i][0] not in N_groups[j]:
                                is_minimal = False
                                break
                    if is_minimal:
                        already_found = False
                        for M in minimal_N:
                            if classes[i][0] in M:
                                already_found = True
                                break
                        if not already_found:
                            minimal_N.append(N_groups[i])
                            
                all_gens = []
                for M in minimal_N:
                    all_gens.extend(M.generators)
                
                if not all_gens:
                    socle_order = 1
                else:
                    socle = PermutationGroup(all_gens)
                    socle_order = socle.order()
                    
                if socle_order == witness.order():
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G contains no non-trivial abelian normal subgroups",
    "¬Q: G is not isomorphic to a direct product of non-abelian simple groups"
]

N_HYP = 2
NEG_Q_INDEX = 2