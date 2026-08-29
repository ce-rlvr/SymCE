import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        G, N = witness
    except Exception:
        return [False, False]
    
    # H1: N is a normal subgroup of G
    try:
        if not N.is_subgroup(G):
            h1 = False
        else:
            try:
                h1 = bool(G.is_normal(N))
            except Exception:
                n_elements_set = set(N.generate())
                h1 = True
                for g in list(G.generate()):
                    g_inv = ~g
                    for n in N.generators:
                        if (g * n * g_inv) not in n_elements_set:
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # neg_Q: C_G(N) is NOT a normal subgroup of G
    try:
        C = None
        if hasattr(G, 'centralizer'):
            try:
                C = G.centralizer(N)
            except Exception:
                pass
        
        if C is None:
            gens = N.generators
            c_elements = []
            for g in list(G.generate()):
                if all(g * n == n * g for n in gens):
                    c_elements.append(g)
            C = PermutationGroup(c_elements)
        
        try:
            is_C_normal = bool(G.is_normal(C))
        except Exception:
            c_elements_set = set(C.generate())
            is_C_normal = True
            for g in list(G.generate()):
                g_inv = ~g
                for c in C.generators:
                    if (g * c * g_inv) not in c_elements_set:
                        is_C_normal = False
                        break
                if not is_C_normal:
                    break
        
        neg_q = not is_C_normal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The centralizer C_G(N) is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1