import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False, False]

    # H1: G and N are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        if h1:
            is_subgroup = N.is_subgroup(G)
            is_normal = True
            if is_subgroup:
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            h2 = is_subgroup and is_normal
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: The center of N is trivial
    try:
        if h1:
            h3 = (N.center().order() == 1)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: G is NOT isomorphic to N \times C_G(N)
    try:
        if h1:
            # Compute C_G(N)
            c_g_n_elements = []
            for g in G.generate():
                commutes = True
                for n in N.generators:
                    if g * n != n * g:
                        commutes = False
                        break
                if commutes:
                    c_g_n_elements.append(g)
            
            if not c_g_n_elements:
                c_g_n_elements = [Permutation()]
                
            C_G_N = PermutationGroup(c_g_n_elements)
            
            # Check orders first for fast rejection
            if G.order() != N.order() * C_G_N.order():
                neg_q = True
            else:
                # Construct external direct product N x C_G(N)
                degN = N.degree
                degC = C_G_N.degree
                
                gens = []
                for g in N.generators:
                    arr = list(g.array_form)
                    if len(arr) < degN:
                        arr += list(range(len(arr), degN))
                    arr += list(range(degN, degN + degC))
                    gens.append(Permutation(arr))
                for g in C_G_N.generators:
                    arr = list(g.array_form)
                    if len(arr) < degC:
                        arr += list(range(len(arr), degC))
                    p = list(range(degN)) + [x + degN for x in arr]
                    gens.append(Permutation(p))
                
                if not gens:
                    gens = [Permutation()]
                    
                NxC = PermutationGroup(gens)
                neg_q = not G.is_isomorphic(NxC)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and N are groups",
    "H_2: N is a normal subgroup of G",
    "H_3: The center of N is trivial",
    "¬Q: G is not isomorphic to N \\times C_G(N)"
]

N_HYP = 3
NEG_Q_INDEX = 3