import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import primefactors
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
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # H1 and H2 are definitions, so we just verify the witness is a valid finite group
        if not isinstance(witness, PermutationGroup):
            return [False, False, False]
        
        elements = list(witness.generate())
        n = len(elements)
        if n < 1:
            return [False, False, False]
            
        h1_ok = True
        h2_ok = True
    except Exception:
        return [False, False, False]
        
    try:
        # Find the identity element
        ident = None
        for e in elements:
            if e * e == e:
                ident = e
                break
        if ident is None:
            return [h1_ok, h2_ok, False]
            
        # Generate all subgroups
        trivial_sub = frozenset([ident])
        subgroups = set([trivial_sub])
        queue = [trivial_sub]
        
        while queue:
            H_elems = queue.pop(0)
            for x in elements:
                if x not in H_elems:
                    new_H = set(H_elems)
                    new_H.add(x)
                    added = True
                    # Close the subset under multiplication
                    while added:
                        added = False
                        current_elements = list(new_H)
                        for a in current_elements:
                            for b in current_elements:
                                c = a * b
                                if c not in new_H:
                                    new_H.add(c)
                                    added = True
                    new_H_frozen = frozenset(new_H)
                    if new_H_frozen not in subgroups:
                        subgroups.add(new_H_frozen)
                        queue.append(new_H_frozen)
                        
        # Find all maximal subgroups
        G_elems = frozenset(elements)
        proper_subs = [H for H in subgroups if H != G_elems]
        maximal_subs = []
        for M in proper_subs:
            is_max = True
            for H in proper_subs:
                if M != H and M.issubset(H):
                    is_max = False
                    break
            if is_max:
                maximal_subs.append(M)
                
        # Compute the Frattini subgroup (intersection of all maximal subgroups)
        if not maximal_subs:
            phi_G = G_elems
        else:
            phi_G = set(maximal_subs[0])
            for M in maximal_subs[1:]:
                phi_G = phi_G.intersection(M)
            phi_G = frozenset(phi_G)
            
        # Compute rad(n)
        if n == 1:
            rad_n = 1
        else:
            factors = primefactors(n)
            rad_n = 1
            for p in factors:
                rad_n *= p
                
        target_order = n // rad_n
        
        # Check negated conclusion: Phi(G) is NOT the unique subgroup of order n/rad(n)
        if len(phi_G) != target_order:
            neg_q = True
        else:
            count = sum(1 for H in subgroups if len(H) == target_order)
            if count != 1:
                neg_q = True
            else:
                neg_q = False
                
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    r"H_1: \Phi(G) is the Frattini subgroup of G, defined as the intersection of all maximal subgroups of G",
    r"H_2: rad(n) is the radical of n, defined as the product of all distinct prime factors of n",
    r"¬Q: \Phi(G) is not the unique subgroup of G of order n/rad(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2