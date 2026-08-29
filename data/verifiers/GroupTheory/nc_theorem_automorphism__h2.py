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
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
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
    try:
        # Witness can be (G, H) or (G, H, N_G(H), C_G(H))
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, H = witness
                N_given = None
                C_given = None
            elif len(witness) == 4:
                G, H, N_given, C_given = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        # H_1: G is a group
        h1 = isinstance(G, PermutationGroup)
        if not h1:
            return [False, False, False, False]
            
        if isinstance(H, PermutationGroup):
            H_elems = list(H.elements)
        else:
            H_elems = list(H)
            
        H_set = set(H_elems)
        G_elems = set(G.elements)
        
        # H must be a subset of G for normalizer and centralizer to be well-defined
        if not H_set.issubset(G_elems):
            return [False, False, False, False]
            
        # Compute the actual normalizer N_G(H)
        N_elems = []
        for g in G_elems:
            conj = set((g * h * ~g) for h in H_set)
            if conj == H_set:
                N_elems.append(g)
        N_actual = PermutationGroup(N_elems)
        
        # Compute the actual centralizer C_G(H)
        C_elems = []
        for g in G_elems:
            if all((g * h == h * g) for h in H_set):
                C_elems.append(g)
        C_actual = PermutationGroup(C_elems)
        
        # H_2: N_G(H) is the normalizer of H in G
        if N_given is not None:
            if not isinstance(N_given, PermutationGroup):
                h2 = False
            else:
                h2 = (set(N_given.elements) == set(N_actual.elements))
        else:
            h2 = True
            
        # H_3: C_G(H) is the centralizer of H in G
        if C_given is not None:
            if not isinstance(C_given, PermutationGroup):
                h3 = False
            else:
                h3 = (set(C_given.elements) == set(C_actual.elements))
        else:
            h3 = True
            
        # Find the identity element of G
        id_elem = next(g for g in G_elems if g * g == g)
        
        # Check if H is a subgroup of G
        is_subgroup = True
        if id_elem not in H_set:
            is_subgroup = False
        else:
            for a in H_set:
                if ~a not in H_set:
                    is_subgroup = False
                    break
                for b in H_set:
                    if (a * b) not in H_set:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
                    
        # ¬Q: The quotient group N_G(H)/C_G(H) is NOT isomorphic to a subgroup of Aut(H).
        # If H is a subgroup, the N/C theorem guarantees N_G(H)/C_G(H) embeds into Aut(H).
        # If H is NOT a subgroup, Aut(H) is undefined, making the conclusion false.
        neg_q = not is_subgroup
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N_G(H) is the normalizer of H in G",
    "H_3: C_G(H) is the centralizer of H in G",
    "¬Q: The quotient group N_G(H)/C_G(H) is not isomorphic to a subgroup of Aut(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3