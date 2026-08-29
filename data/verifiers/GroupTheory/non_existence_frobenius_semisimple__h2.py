import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_finite_group(G):
    try:
        if not isinstance(G, PermutationGroup):
            return False
        return G.order() < float('inf')
    except Exception:
        return False

def is_frobenius_group(G):
    try:
        if not hasattr(G, 'elements') or not hasattr(G, 'order'):
            return False
        order = G.order()
        if order <= 1 or order == float('inf'):
            return False
            
        elements = list(G.elements)
        id_el = G.identity
        
        # Generate all cyclic subgroups
        cyclic_subgroups = set()
        for g in elements:
            if g == id_el:
                continue
            H = set()
            curr = g
            while curr not in H:
                H.add(curr)
                curr = curr * g
            cyclic_subgroups.add(frozenset(H))
            
        # Check cyclic subgroups first (covers most common Frobenius complements)
        for H in cyclic_subgroups:
            if len(H) <= 1 or len(H) >= order:
                continue
            
            is_frobenius_complement = True
            for x in elements:
                if x in H:
                    continue
                x_inv = ~x
                intersection_size = 0
                for h in H:
                    conj = x * h * x_inv
                    if conj in H:
                        intersection_size += 1
                        if intersection_size > 1:
                            is_frobenius_complement = False
                            break
                if not is_frobenius_complement:
                    break
            if is_frobenius_complement:
                return True
                
        # Fallback to 2-generated subgroups for small groups
        if order <= 50:
            subgroups_to_check = set()
            for H1 in cyclic_subgroups:
                for H2 in cyclic_subgroups:
                    if H1 != H2:
                        new_H = set(H1 | H2)
                        added = True
                        while added:
                            added = False
                            next_H = set(new_H)
                            for a in new_H:
                                for b in new_H:
                                    c = a * b
                                    if c not in next_H:
                                        next_H.add(c)
                                        added = True
                            new_H = next_H
                        if len(new_H) < order:
                            subgroups_to_check.add(frozenset(new_H))
                            
            for H in subgroups_to_check:
                if len(H) <= 1 or len(H) >= order:
                    continue
                
                is_frobenius_complement = True
                for x in elements:
                    if x in H:
                        continue
                    x_inv = ~x
                    intersection_size = 0
                    for h in H:
                        conj = x * h * x_inv
                        if conj in H:
                            intersection_size += 1
                            if intersection_size > 1:
                                is_frobenius_complement = False
                                break
                    if not is_frobenius_complement:
                        break
                if is_frobenius_complement:
                    return True
                    
        return False
    except Exception:
        return False

def conditions(witness):
    return [
        is_finite_group(witness),
        is_frobenius_group(witness)
    ]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G is a Frobenius group"
]

N_HYP = 1
NEG_Q_INDEX = 1