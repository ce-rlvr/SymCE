import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, H, f_obj = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # Define f safely
    f = None
    if callable(f_obj):
        f = f_obj
    elif isinstance(f_obj, dict):
        f = lambda x: f_obj[x]

    # H_2: f is a group homomorphism from G to H
    try:
        h2 = False
        if h1 and f is not None:
            g_elements = list(G.generate())
            valid_mapping = True
            for g in g_elements:
                try:
                    val = f(g)
                    if val not in H:
                        valid_mapping = False
                        break
                except Exception:
                    valid_mapping = False
                    break
            
            if valid_mapping:
                is_hom = True
                for x in g_elements:
                    for y in g_elements:
                        if f(x * y) != f(x) * f(y):
                            is_hom = False
                            break
                    if not is_hom:
                        break
                h2 = is_hom
    except Exception:
        h2 = False

    # neg_Q: The image f(G) is not an abelian subgroup of H
    try:
        neg_q = False
        if h1 and f is not None:
            image_elements = []
            for g in list(G.generate()):
                try:
                    image_elements.append(f(g))
                except Exception:
                    pass
            
            if image_elements:
                is_abelian = True
                for a in image_elements:
                    for b in image_elements:
                        if a * b != b * a:
                            is_abelian = False
                            break
                    if not is_abelian:
                        break
                neg_q = not is_abelian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a group homomorphism from G to H",
    "¬Q: The image f(G) is not an abelian subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2