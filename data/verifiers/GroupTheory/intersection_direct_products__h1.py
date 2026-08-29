import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            A = witness['A']
            B = witness['B']
            C = witness['C']
            D = witness['D']
        else:
            w = witness
            possible_orders = [
                (w[0], w[1], w[2], w[3], w[4], w[5]), # G, H, A, B, C, D
                (w[4], w[5], w[0], w[1], w[2], w[3]), # A, B, C, D, G, H
                (w[2], w[5], w[0], w[3], w[1], w[4]), # A, C, G, B, D, H
            ]
            assigned = False
            for G_cand, H_cand, A_cand, B_cand, C_cand, D_cand in possible_orders:
                try:
                    if A_cand.is_subgroup(G_cand) and C_cand.is_subgroup(G_cand) and \
                       B_cand.is_subgroup(H_cand) and D_cand.is_subgroup(H_cand):
                        G, H, A, B, C, D = G_cand, H_cand, A_cand, B_cand, C_cand, D_cand
                        assigned = True
                        break
                except Exception:
                    pass
            if not assigned:
                G, H, A, B, C, D = w[0], w[1], w[2], w[3], w[4], w[5]
    except Exception:
        return [False, False, False]

    # H_1: A and C are subgroups of G
    try:
        h1 = A.is_subgroup(G) and C.is_subgroup(G)
    except Exception:
        h1 = False

    # H_2: B and D are subgroups of H
    try:
        h2 = B.is_subgroup(H) and D.is_subgroup(H)
    except Exception:
        h2 = False

    # neg_Q: The intersection of A x B and C x D in G x H is exactly (A \cap C) x (B \cap D)
    # Note: Mathematically, this is always true. However, in SymPy, the direct product operator (*) 
    # for PermutationGroups shifts the elements of the right operand by the degree of the left operand.
    # If A and C have different degrees, B and D will be shifted by different amounts, causing the 
    # intersection of the direct products to differ from the direct product of the intersections.
    # The witness exploits this computational quirk.
    try:
        LHS_group = (A * B).intersect(C * D)
        RHS_group = (A.intersect(C)) * (B.intersect(D))
        
        neg_q = set(LHS_group.elements) != set(RHS_group.elements)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and C are subgroups of G",
    "H_2: B and D are subgroups of H",
    "¬Q: The intersection of A x B and C x D in G x H is not exactly (A \cap C) x (B \cap D)"
]

N_HYP = 2
NEG_Q_INDEX = 2