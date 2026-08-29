import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_quotient_group(N, H):
    elements_N = list(N.elements)
    elements_H = list(H.elements)
    
    cosets_sets = []
    cosets_reps = []
    seen = set()
    for n in elements_N:
        if n not in seen:
            coset_set = set()
            rep = None
            for h in elements_H:
                nh = n * h
                if rep is None:
                    rep = nh
                coset_set.add(nh)
                seen.add(nh)
            cosets_sets.append(coset_set)
            cosets_reps.append(rep)
            
    k = len(cosets_sets)
    if k == 1:
        return PermutationGroup([Permutation(0)])
        
    perms = []
    for g in N.generators:
        p = []
        for i in range(k):
            c = cosets_reps[i]
            gc = g * c
            for j in range(k):
                if gc in cosets_sets[j]:
                    p.append(j)
                    break
        perms.append(Permutation(p))
        
    return PermutationGroup(perms)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                G, H, N, A = witness
            elif len(witness) == 3:
                G, H, A = witness
                if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)):
                    return [False, False, False, False]
                norm_elems = [g for g in list(G.elements) if all((g * h * ~g) in H for h in H.generators)]
                N = PermutationGroup(norm_elems)
            elif len(witness) == 2:
                G, H = witness
                if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)):
                    return [False, False, False, False]
                norm_elems = [g for g in list(G.elements) if all((g * h * ~g) in H for h in H.generators)]
                N = PermutationGroup(norm_elems)
                A = get_quotient_group(N, H)
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    try:
        if isinstance(N, PermutationGroup) and N.is_subgroup(G):
            normalizes = True
            for n in list(N.elements):
                for h in H.generators:
                    if (n * h * ~n) not in H:
                        normalizes = False
                        break
                if not normalizes:
                    break
            
            maximal = True
            if normalizes:
                for g in list(G.elements):
                    if g not in N:
                        g_normalizes = True
                        for h in H.generators:
                            if (g * h * ~g) not in H:
                                g_normalizes = False
                                break
                        if g_normalizes:
                            maximal = False
                            break
            h3 = normalizes and maximal
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        if not isinstance(A, PermutationGroup):
            neg_q = False
        else:
            Q = get_quotient_group(N, H)
            neg_q = not A.is_isomorphic(Q)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a finite Galois extension of a field F",
    "H_2: E is an intermediate field between F and K",
    "H_3: N_G(H) is the normalizer of H in G",
    "¬Q: Aut(E/F) is NOT isomorphic to N_G(H)/H"
]

N_HYP = 3
NEG_Q_INDEX = 3