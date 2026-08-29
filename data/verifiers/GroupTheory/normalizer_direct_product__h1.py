import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
        G, H, A, B = witness
    except Exception:
        return [False, False, False]
        
    # H1: A is a subgroup of G
    try:
        h1 = True
        for gen in A.generators:
            if not G.contains(gen):
                h1 = False
                break
    except Exception:
        h1 = False

    # H2: B is a subgroup of H
    try:
        h2 = True
        for gen in B.generators:
            if not H.contains(gen):
                h2 = False
                break
    except Exception:
        h2 = False

    # neg_Q: N_{G x H}(A x B) != N_G(A) x N_H(B)
    try:
        G_elems = list(G.generate_dimino())
        H_elems = list(H.generate_dimino())
        
        N_G_A = []
        for g in G_elems:
            g_inv = g**-1
            is_norm = True
            for a in A.generators:
                if not A.contains(g * a * g_inv):
                    is_norm = False
                    break
            if is_norm:
                N_G_A.append(g)
                
        N_H_B = []
        for h in H_elems:
            h_inv = h**-1
            is_norm = True
            for b in B.generators:
                if not B.contains(h * b * h_inv):
                    is_norm = False
                    break
            if is_norm:
                N_H_B.append(h)
                
        N_GxH_AxB = []
        for g in G_elems:
            g_inv = g**-1
            for h in H_elems:
                h_inv = h**-1
                is_norm = True
                for a in A.generators:
                    if not A.contains(g * a * g_inv):
                        is_norm = False
                        break
                if is_norm:
                    for b in B.generators:
                        if not B.contains(h * b * h_inv):
                            is_norm = False
                            break
                if is_norm:
                    N_GxH_AxB.append((g, h))
                    
        N_G_A_x_N_H_B = [(g, h) for g in N_G_A for h in N_H_B]
        
        if len(N_GxH_AxB) != len(N_G_A_x_N_H_B):
            neg_q = True
        else:
            neg_q = False
            for pair in N_GxH_AxB:
                if pair not in N_G_A_x_N_H_B:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a subgroup of G",
    "H_2: B is a subgroup of H",
    "¬Q: The normalizer of A x B in G x H is not equal to N_G(A) x N_H(B)"
]

N_HYP = 2
NEG_Q_INDEX = 2