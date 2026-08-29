import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.abc
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def eval_f(f, x):
    try:
        return f(x)
    except TypeError:
        return f[x]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            A = witness.get('A')
            B = witness.get('B')
            f = witness.get('f')
        else:
            G = getattr(witness, 'G', None)
            H = getattr(witness, 'H', None)
            A = getattr(witness, 'A', None)
            B = getattr(witness, 'B', None)
            f = getattr(witness, 'f', None)
    except Exception:
        return [False, False, False, False]

    # H1: G and H are groups
    try:
        h1 = (getattr(G, 'is_group', False) or isinstance(G, PermutationGroup)) and \
             (getattr(H, 'is_group', False) or isinstance(H, PermutationGroup))
    except Exception:
        h1 = False

    # H2: A and B are subgroups of G
    try:
        h2 = A.is_subgroup(G) and B.is_subgroup(G)
    except Exception:
        h2 = False

    # H3: ker(f) is a subset of A
    try:
        H_id = H.identity
        ker_f = set()
        for g in G.elements:
            if eval_f(f, g) == H_id:
                ker_f.add(g)
        h3 = ker_f.issubset(set(A.elements))
    except Exception:
        h3 = False

    # neg_Q: f(A ∩ B) != f(A) ∩ f(B)
    try:
        A_elements = set(A.elements)
        B_elements = set(B.elements)
        A_int_B = A_elements.intersection(B_elements)
        
        f_A = {eval_f(f, x) for x in A_elements}
        f_B = {eval_f(f, x) for x in B_elements}
        f_A_int_B = {eval_f(f, x) for x in A_int_B}
        
        neg_q = f_A_int_B != f_A.intersection(f_B)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: A and B are subgroups of G",
    "H_3: ker(f) is a subset of A",
    "¬Q: f(A ∩ B) != f(A) ∩ f(B)"
]

N_HYP = 3
NEG_Q_INDEX = 3