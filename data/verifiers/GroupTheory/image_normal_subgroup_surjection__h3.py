import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import math
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
            N = witness.get('N')
        else:
            G, H, f, N = witness
    except Exception:
        return [False, False, False]

    try:
        g_elements = list(G.elements)
        h_elements = list(H.elements)
    except Exception:
        return [False, False, False]

    try:
        f_map = {}
        if isinstance(f, dict):
            f_map = f
        else:
            for g in g_elements:
                f_map[g] = f(g)
    except Exception:
        f_map = {}

    # H1: G and H are groups, and N is a subgroup of G
    try:
        h1 = True
        if hasattr(N, 'elements'):
            n_elements = list(N.elements)
        else:
            n_elements = list(N)
            
        if not all(n in g_elements for n in n_elements):
            h1 = False
        else:
            is_N_subgroup = True
            if len(n_elements) == 0:
                is_N_subgroup = False
            else:
                for x in n_elements:
                    for y in n_elements:
                        if x * y not in n_elements:
                            is_N_subgroup = False
                            break
                    if not is_N_subgroup:
                        break
            h1 = h1 and is_N_subgroup
    except Exception:
        h1 = False

    # H2: f: G \to H is a surjective group homomorphism
    try:
        if not all(g in f_map for g in g_elements):
            h2 = False
        else:
            is_homo = True
            for g1 in g_elements:
                for g2 in g_elements:
                    if f_map[g1 * g2] != f_map[g1] * f_map[g2]:
                        is_homo = False
                        break
                if not is_homo:
                    break
                    
            image = set(f_map[g] for g in g_elements)
            is_surj = (image == set(h_elements))
            
            h2 = is_homo and is_surj
    except Exception:
        h2 = False

    # neg_Q: The image f(N) is not a normal subgroup of H
    try:
        if not all(n in f_map for n in n_elements):
            neg_q = False
        else:
            f_N = set(f_map[n] for n in n_elements)
            
            is_subgroup = True
            if len(f_N) == 0:
                is_subgroup = False
            else:
                for x in f_N:
                    for y in f_N:
                        if x * y not in f_N:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                        
            if not is_subgroup:
                neg_q = True
            else:
                is_normal = True
                for h in h_elements:
                    h_inv = h**-1
                    for n_val in f_N:
                        if h * n_val * h_inv not in f_N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups, and N is a subgroup of G",
    "H_2: f: G \\to H is a surjective group homomorphism",
    "¬Q: The image f(N) is not a normal subgroup of H"
]
N_HYP = 2
NEG_Q_INDEX = 2