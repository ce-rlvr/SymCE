import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy import lcm

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is the semidirect product of a normal subgroup N and a subgroup H",
    "H_2: H has finite exponent e_H",
    "¬Q: The exponent of G does not divide e_N * e_H"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_exponent(grp):
    e = 1
    for g in grp.elements:
        e = lcm(e, g.order())
    return e

def conditions(witness):
    try:
        G = witness[0]
        N = witness[1]
        H = witness[2]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = False
        if all(g in G for g in N.generators) and all(g in G for g in H.generators):
            is_normal = True
            for n in N.generators:
                for g in G.generators:
                    if (~g * n * g) not in N:
                        is_normal = False
                        break
                    if (g * n * ~g) not in N:
                        is_normal = False
                        break
                if not is_normal:
                    break
            if is_normal:
                if N.order() * H.order() == G.order():
                    intersection = set(N.elements).intersection(set(H.elements))
                    if len(intersection) == 1:
                        h1 = True
    except Exception:
        h1 = False

    try:
        e_H = get_exponent(H)
        h2 = (e_H > 0)
    except Exception:
        h2 = False

    try:
        e_G = get_exponent(G)
        e_N = get_exponent(N)
        e_H = get_exponent(H)
        neg_q = ((e_N * e_H) % e_G != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]