import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_all_subgroups(G):
    """Computes all subgroups of a finite group G by closing cyclic subgroups under joins."""
    if hasattr(G, 'order'):
        if callable(G.order):
            order = G.order()
        else:
            order = G.order
        if order > 200:
            raise ValueError("Group too large to compute subgroup lattice")
            
    try:
        elements = list(G.elements)
    except Exception:
        elements = list(G.generate())
        
    subgroups = []
    
    # Generate all cyclic subgroups
    for g in elements:
        sub = set()
        curr = g
        while curr not in sub:
            sub.add(curr)
            curr = curr * g
        if sub not in subgroups:
            subgroups.append(sub)
            
    # Close under joins
    changed = True
    while changed:
        changed = False
        new_subgroups = []
        for H in subgroups:
            for K in subgroups:
                join_set = H.union(K)
                closure = set(join_set)
                added = True
                while added:
                    added = False
                    new_elements = set()
                    for x in closure:
                        for y in closure:
                            xy = x * y
                            if xy not in closure and xy not in new_elements:
                                new_elements.add(xy)
                    if new_elements:
                        closure.update(new_elements)
                        added = True
                if closure not in subgroups and closure not in new_subgroups:
                    new_subgroups.append(closure)
                    changed = True
        if changed:
            subgroups.extend(new_subgroups)
            
    return subgroups

def is_distributive(subgroups):
    """Checks if the lattice of subgroups is distributive."""
    sub_list = [frozenset(s) for s in subgroups]
    sorted_sub_list = sorted(sub_list, key=len)
    
    # Precompute joins
    join_dict = {}
    for i, s1 in enumerate(sorted_sub_list):
        for s2 in sorted_sub_list[i:]:
            union = s1.union(s2)
            for s in sorted_sub_list:
                if union.issubset(s):
                    join_dict[(s1, s2)] = s
                    join_dict[(s2, s1)] = s
                    break
                    
    # Check distributive law: A ∩ (B ∨ C) = (A ∩ B) ∨ (A ∩ C)
    for A in sorted_sub_list:
        for B in sorted_sub_list:
            for C in sorted_sub_list:
                B_join_C = join_dict[(B, C)]
                left = A.intersection(B_join_C)
                
                A_cap_B = A.intersection(B)
                A_cap_C = A.intersection(C)
                right = join_dict[(A_cap_B, A_cap_C)]
                
                if left != right:
                    return False
    return True

def conditions(witness) -> list[bool]:
    # H_1: The lattice of subgroups of G under inclusion is a distributive lattice
    try:
        if hasattr(witness, 'subgroup_lattice_is_distributive'):
            if callable(witness.subgroup_lattice_is_distributive):
                h1 = witness.subgroup_lattice_is_distributive()
            else:
                h1 = witness.subgroup_lattice_is_distributive
        elif hasattr(witness, 'has_distributive_subgroup_lattice'):
            if callable(witness.has_distributive_subgroup_lattice):
                h1 = witness.has_distributive_subgroup_lattice()
            else:
                h1 = witness.has_distributive_subgroup_lattice
        else:
            subgroups = get_all_subgroups(witness)
            h1 = is_distributive(subgroups)
    except Exception:
        h1 = False

    # ¬Q: G is NOT a locally cyclic group
    try:
        if hasattr(witness, 'is_locally_cyclic'):
            if callable(witness.is_locally_cyclic):
                neg_q = not witness.is_locally_cyclic()
            else:
                neg_q = not witness.is_locally_cyclic
        elif hasattr(witness, 'is_cyclic'):
            # For finite groups, locally cyclic is equivalent to cyclic
            if callable(witness.is_cyclic):
                neg_q = not witness.is_cyclic()
            else:
                neg_q = not witness.is_cyclic
        else:
            # Fallback: locally cyclic implies abelian.
            if callable(witness.is_abelian):
                neg_q = not witness.is_abelian()
            else:
                neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The lattice of subgroups of G under inclusion is a distributive lattice",
    "¬Q: G is not a locally cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1