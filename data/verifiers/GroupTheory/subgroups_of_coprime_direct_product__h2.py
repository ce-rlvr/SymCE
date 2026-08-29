import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H, S = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are finite groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: S is a subgroup of G x H
    try:
        if not isinstance(S, PermutationGroup):
            h2 = False
        else:
            n = G.degree
            m = H.degree
            h2 = True
            for gen in S.generators:
                arr = gen.array_form
                if len(arr) > n + m:
                    h2 = False
                    break
                # Pad the array form to the full degree of G x H
                arr = arr + list(range(len(arr), n + m))
                
                # Check block preservation (G acts on 0..n-1, H acts on n..n+m-1)
                if any(arr[i] >= n for i in range(n)):
                    h2 = False
                    break
                if any(arr[i] < n for i in range(n, n + m)):
                    h2 = False
                    break
                    
                arr_G = arr[:n]
                arr_H = [x - n for x in arr[n:n+m]]
                
                if Permutation(arr_G) not in G:
                    h2 = False
                    break
                if Permutation(arr_H) not in H:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: S is NOT of the form A x B for any A <= G, B <= H
    try:
        if not isinstance(S, PermutationGroup) or not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            neg_q = False
        else:
            n = G.degree
            m = H.degree
            gens_G = []
            gens_H = []
            for gen in S.generators:
                arr = gen.array_form
                arr = arr + list(range(len(arr), n + m))
                arr_G = arr[:n]
                arr_H = [x - n for x in arr[n:n+m]]
                gens_G.append(Permutation(arr_G))
                gens_H.append(Permutation(arr_H))
            
            if not gens_G:
                gens_G = [Permutation(n - 1) if n > 0 else Permutation()]
            if not gens_H:
                gens_H = [Permutation(m - 1) if m > 0 else Permutation()]
                
            proj_G = PermutationGroup(gens_G)
            proj_H = PermutationGroup(gens_H)
            
            # S is of the form A x B iff S is exactly the direct product of its projections.
            # Since S is a subgroup of proj_G x proj_H, equality holds iff their orders match.
            neg_q = S.order() != proj_G.order() * proj_H.order()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: S is a subgroup of G x H",
    "¬Q: S is not of the form A x B for any A <= G, B <= H"
]

N_HYP = 2
NEG_Q_INDEX = 2