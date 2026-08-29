import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    try:
        G, A, A_star, B, B_star = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = hasattr(G, 'is_group') and G.is_group
        if not hasattr(G, 'is_group'):
            h1 = hasattr(G, 'generators') or hasattr(G, 'elements')
    except Exception:
        h1 = False
        
    # H2: A^* is a normal subgroup of A
    try:
        h2 = A_star.is_subgroup(A) and A_star.is_normal(A)
    except Exception:
        h2 = False
        
    # H3: B^* is a normal subgroup of B
    try:
        h3 = B_star.is_subgroup(B) and B_star.is_normal(B)
    except Exception:
        h3 = False
        
    # neg_Q: conclusion fails
    try:
        A_cap_B = A.intersect(B)
        A_cap_B_star = A.intersect(B_star)
        A_star_cap_B = A_star.intersect(B)
        
        def generate_subgroup(g1, g2):
            if hasattr(g1, 'generators') and hasattr(g2, 'generators'):
                gens = list(g1.generators) + list(g2.generators)
                return PermutationGroup(gens)
            return g1 * g2
            
        LHS_num = generate_subgroup(A_cap_B, A_star)
        LHS_den = generate_subgroup(A_cap_B_star, A_star)
        
        RHS_num = generate_subgroup(A_cap_B, B_star)
        RHS_den = generate_subgroup(A_star_cap_B, B_star)
        
        if not LHS_den.is_subgroup(LHS_num) or not LHS_den.is_normal(LHS_num):
            neg_q = True
        elif not RHS_den.is_subgroup(RHS_num) or not RHS_den.is_normal(RHS_num):
            neg_q = True
        else:
            LHS_q = LHS_num.quotient_group(LHS_den)
            RHS_q = RHS_num.quotient_group(RHS_den)
            q_holds = LHS_q.is_isomorphic(RHS_q)
            neg_q = not q_holds
    except Exception:
        neg_q = True
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: A^* is a normal subgroup of A",
    "H_3: B^* is a normal subgroup of B",
    "¬Q: The quotient groups are not isomorphic or undefined"
]

N_HYP = 3
NEG_Q_INDEX = 3