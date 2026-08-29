import math
import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            H1 = witness.get('H1')
            H2 = witness.get('H2')
        else:
            G, N, H1, H2 = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h1 = False
        
    try:
        ord_G = G.order() if callable(G.order) else G.order
        ord_N = N.order() if callable(N.order) else N.order
        if ord_G % ord_N == 0:
            idx = ord_G // ord_N
            h2 = math.gcd(ord_N, idx) == 1
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        solv_N = N.is_solvable
        if callable(solv_N): solv_N = solv_N()
        solv_G = G.is_solvable
        if callable(solv_G): solv_G = solv_G()
        
        ord_G = G.order() if callable(G.order) else G.order
        ord_N = N.order() if callable(N.order) else N.order
        
        if solv_N:
            h3 = True
        elif solv_G:
            h3 = True
        elif ord_N % 2 != 0:
            h3 = True
        elif (ord_G // ord_N) % 2 != 0:
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False
        
    try:
        ord_G = G.order() if callable(G.order) else G.order
        ord_N = N.order() if callable(N.order) else N.order
        ord_H1 = H1.order() if callable(H1.order) else H1.order
        ord_H2 = H2.order() if callable(H2.order) else H2.order
        
        if not (H1.is_subgroup(G) and H2.is_subgroup(G)):
            neg_q = False
        elif ord_H1 * ord_N != ord_G or ord_H2 * ord_N != ord_G:
            neg_q = False
        else:
            gen1 = list(H1.generators) + list(N.generators)
            if not gen1:
                order1 = 1
            else:
                pg1 = PermutationGroup(*gen1)
                order1 = pg1.order() if callable(pg1.order) else pg1.order
                
            gen2 = list(H2.generators) + list(N.generators)
            if not gen2:
                order2 = 1
            else:
                pg2 = PermutationGroup(*gen2)
                order2 = pg2.order() if callable(pg2.order) else pg2.order
                
            if order1 != ord_G or order2 != ord_G:
                neg_q = False
            else:
                are_conj = False
                for g in G.generate():
                    g_inv = ~g
                    maps_to_H2 = True
                    for h in H1.generators:
                        if (g * h * g_inv) not in H2:
                            maps_to_H2 = False
                            break
                    if maps_to_H2:
                        are_conj = True
                        break
                neg_q = not are_conj
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: The order of N and the index of N in G are coprime",
    "H_3: Either N or G/N is a solvable group",
    "not Q: There exist two subgroups of G that are complements of N in G but are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3