import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
        G, A, B = witness
    except Exception:
        return [False, False, False]
        
    # H1: A and B are subsets of G
    try:
        if hasattr(G, 'elements'):
            G_elements = list(G.elements)
        else:
            G_elements = list(G)
            
        try:
            A_col = set(A)
            B_col = set(B)
            G_col = set(G_elements)
            h1 = A_col.issubset(G_col) and B_col.issubset(G_col)
        except TypeError:
            A_col = list(A)
            B_col = list(B)
            G_col = list(G_elements)
            h1 = all(a in G_col for a in A_col) and all(b in G_col for b in B_col)
    except Exception:
        h1 = False
        A_col = []
        B_col = []
        G_elements = []

    # H2: A and B are each a union of conjugacy classes of G
    try:
        def is_union_of_conjugacy_classes(S_col):
            for s in S_col:
                for g in G_elements:
                    try:
                        conj = g**-1 * s * g
                    except Exception:
                        conj = ~g * s * g
                    if conj not in S_col:
                        return False
            return True
            
        h2 = is_union_of_conjugacy_classes(A_col) and is_union_of_conjugacy_classes(B_col)
    except Exception:
        h2 = False

    # neg_Q: AB is NOT a union of conjugacy classes of G
    try:
        try:
            AB_col = set()
            for a in A_col:
                for b in B_col:
                    AB_col.add(a * b)
        except TypeError:
            AB_col = []
            for a in A_col:
                for b in B_col:
                    prod = a * b
                    if prod not in AB_col:
                        AB_col.append(prod)
                        
        is_union = True
        for s in AB_col:
            for g in G_elements:
                try:
                    conj = g**-1 * s * g
                except Exception:
                    conj = ~g * s * g
                if conj not in AB_col:
                    is_union = False
                    break
            if not is_union:
                break
                
        neg_q = not is_union
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are subsets of G",
    "H_2: A and B are each a union of conjugacy classes of G",
    "¬Q: AB is not a union of conjugacy classes of G"
]

N_HYP = 2
NEG_Q_INDEX = 2