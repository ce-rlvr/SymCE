import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Inn(G) is the group of inner automorphisms of G",
    "¬Q: G/Z(G) is not isomorphic to Inn(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # H_2 is a definitional hypothesis. If G is a group, Inn(G) is well-defined.
        h2 = h1
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            G = witness
            elements = list(G.generate())
            
            # Find center Z(G)
            center_elems = []
            for g in elements:
                if all(g * x == x * g for x in elements):
                    center_elems.append(g)
            Z = PermutationGroup(center_elems)
            
            # Construct G/Z(G)
            n_elements = list(Z.generate())
            cosets = []
            coset_reps = []
            seen = set()
            for g in elements:
                if g not in seen:
                    coset = frozenset(g * n for n in n_elements)
                    cosets.append(coset)
                    coset_reps.append(g)
                    seen.update(coset)
                    
            elem_to_coset_idx = {}
            for i, coset in enumerate(cosets):
                for e in coset:
                    elem_to_coset_idx[e] = i
                    
            g_mod_z_perms = []
            for g in elements:
                p = [0] * len(cosets)
                for i, rep in enumerate(coset_reps):
                    prod = g * rep
                    p[i] = elem_to_coset_idx[prod]
                g_mod_z_perms.append(Permutation(p))
            G_mod_Z = PermutationGroup(g_mod_z_perms)
            
            # Construct Inn(G)
            elem_to_idx = {e: i for i, e in enumerate(elements)}
            inn_perms = []
            for g in elements:
                p = [0] * len(elements)
                for x in elements:
                    y = g * x * ~g
                    p[elem_to_idx[x]] = elem_to_idx[y]
                inn_perms.append(Permutation(p))
            Inn_G = PermutationGroup(inn_perms)
            
            # Check isomorphism
            is_iso = G_mod_Z.is_isomorphic(Inn_G)
            neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]