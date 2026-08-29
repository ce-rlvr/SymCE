import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    # H_1: The automorphism group of G is the trivial group
    try:
        h1 = False
        if isinstance(witness, PermutationGroup):
            # We check if Aut(G) is trivial by looking for known types of non-trivial automorphisms.
            
            # 1. Inner automorphisms: exist if G is not abelian
            has_nontrivial_inner = not witness.is_abelian
            
            # 2. Inversion automorphism: x -> x^-1 is a non-trivial automorphism for abelian groups if any x != x^-1
            has_nontrivial_inversion = False
            if not has_nontrivial_inner:
                elements = list(witness.generate())
                has_nontrivial_inversion = any(g != g**-1 for g in elements)
            
            # 3. Basis permutation automorphisms: if G is an elementary abelian 2-group of order > 2,
            # it is a vector space over F_2 of dimension >= 2, so GL(V) is non-trivial.
            has_nontrivial_basis_perm = False
            if not has_nontrivial_inner and not has_nontrivial_inversion:
                if witness.order() > 2:
                    has_nontrivial_basis_perm = True
            
            # If any non-trivial automorphism exists, Aut(G) is not trivial.
            if not (has_nontrivial_inner or has_nontrivial_inversion or has_nontrivial_basis_perm):
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: G is NOT isomorphic to either the trivial group or the cyclic group of order 2
    try:
        neg_q = False
        if isinstance(witness, PermutationGroup):
            # The only groups of order <= 2 are the trivial group and Z_2.
            if witness.order() > 2:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The automorphism group of G is the trivial group",
    "¬Q: G is not isomorphic to either the trivial group or the cyclic group of order 2"
]

N_HYP = 1
NEG_Q_INDEX = 1