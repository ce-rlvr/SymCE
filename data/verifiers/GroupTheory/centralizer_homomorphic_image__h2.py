import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        G, H, f = witness
    except Exception:
        return [False, False, False, False]

    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
        if h1:
            G_elems = list(G.elements)
            H_elems = list(H.elements)
            f_G_list = []
            for g in G_elems:
                val = f[g] if isinstance(f, dict) else f(g)
                if val not in H_elems:
                    h1 = False
                    break
                f_G_list.append(val)
    except Exception:
        h1 = False

    # H2: Z(G) is the center of G
    # This is a definitional hypothesis; it holds trivially if H1 holds.
    h2 = h1

    # H3: C_H(f(G)) is the centralizer of the subgroup f(G) in H
    # This implies f(G) must be a valid subgroup of H.
    try:
        if not h1:
            h3 = False
        else:
            f_G_set = set(f_G_list)
            h3 = True
            for x in f_G_set:
                if ~x not in f_G_set:
                    h3 = False
                    break
                for y in f_G_set:
                    if x * y not in f_G_set:
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # neg_Q: f(Z(G)) is NOT a subset of C_H(f(G))
    try:
        if not h1:
            neg_q = False
        else:
            G_elems = list(G.elements)
            H_elems = list(H.elements)
            
            Z_G = []
            for g in G_elems:
                if all(g * x == x * g for x in G_elems):
                    Z_G.append(g)
            
            f_G_set = set(f_G_list)
            C_H = set()
            for h in H_elems:
                if all(h * y == y * h for y in f_G_set):
                    C_H.add(h)
            
            neg_q = False
            for z in Z_G:
                val = f[z] if isinstance(f, dict) else f(z)
                if val not in C_H:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: Z(G) is the center of G",
    "H_3: C_H(f(G)) is the centralizer of the subgroup f(G) in H",
    "¬Q: f(Z(G)) is not a subset of C_H(f(G))"
]

N_HYP = 3
NEG_Q_INDEX = 3