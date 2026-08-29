import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a surjective group homomorphism from G to H",
    "¬Q: f(N_G(S)) is not a subset of N_H(f(S))"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        G = witness['G']
        H = witness['H']
        f = witness['f']
        S = witness['S']
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: f is a surjective group homomorphism from G to H
    try:
        h2 = False
        if h1:
            G_elems = list(G.elements)
            H_elems = list(H.elements)
            
            f_map = {}
            for g in G_elems:
                try:
                    f_map[g] = f[g]
                except (TypeError, KeyError):
                    f_map[g] = f(g)
                    
            if all(f_map[g] in H_elems for g in G_elems):
                image = set(f_map[g] for g in G_elems)
                if image == set(H_elems):
                    is_hom = True
                    for g1 in G_elems:
                        for g2 in G_elems:
                            if f_map[g1 * g2] != f_map[g1] * f_map[g2]:
                                is_hom = False
                                break
                        if not is_hom:
                            break
                    h2 = is_hom
    except Exception:
        h2 = False
        
    # ¬Q: f(N_G(S)) is not a subset of N_H(f(S))
    try:
        neg_q = False
        if h1:
            G_elems = list(G.elements)
            f_map = {}
            for g in G_elems:
                try:
                    f_map[g] = f[g]
                except (TypeError, KeyError):
                    f_map[g] = f(g)
                    
            try:
                S_elems = set(S.elements)
            except AttributeError:
                S_elems = set(S)
                
            if S_elems.issubset(set(G_elems)):
                N_G_S = []
                for g in G_elems:
                    g_inv = g**-1
                    conj = set(g * s * g_inv for s in S_elems)
                    if conj == S_elems:
                        N_G_S.append(g)
                        
                f_S = set(f_map[s] for s in S_elems)
                
                N_H_fS = []
                for h in H.elements:
                    h_inv = h**-1
                    conj = set(h * fs * h_inv for fs in f_S)
                    if conj == f_S:
                        N_H_fS.append(h)
                        
                f_N_G_S = set(f_map[g] for g in N_G_S)
                
                neg_q = not f_N_G_S.issubset(set(N_H_fS))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]