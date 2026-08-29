import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G', [])
            X = witness.get('X', [])
            Y = witness.get('Y', [])
        else:
            G, X, Y = witness
    except Exception:
        return [False, False]

    # H_1: Y is a subset of X
    try:
        h1 = all(y in X for y in Y)
    except Exception:
        h1 = False

    # neg_Q: G_Y is not a subgroup of G
    try:
        def apply_g(g, y):
            if isinstance(g, dict):
                return g[y]
            try:
                return g(y)
            except TypeError:
                return g * y

        G_list = list(G)
        G_Y = []
        for g in G_list:
            image = []
            valid_action = True
            for y in Y:
                try:
                    img = apply_g(g, y)
                    image.append(img)
                except Exception:
                    valid_action = False
                    break
            if not valid_action:
                continue
            
            try:
                is_eq = sorted(image) == sorted(Y)
            except Exception:
                is_eq = len(image) == len(Y) and all(y in image for y in Y) and all(img in Y for img in image)
                
            if is_eq:
                G_Y.append(g)
                
        def is_group(elements):
            if isinstance(elements, sympy.combinatorics.PermutationGroup):
                return True
            elements_list = list(elements)
            if not elements_list:
                return False
            for a in elements_list:
                for b in elements_list:
                    try:
                        ab = a * b
                    except Exception:
                        return False
                    if ab not in elements_list:
                        return False
                try:
                    inv_a = ~a
                except Exception:
                    try:
                        inv_a = a.inv()
                    except Exception:
                        try:
                            inv_a = a**-1
                        except Exception:
                            return False
                if inv_a not in elements_list:
                    return False
            return True

        # The conclusion is that G_Y is a subgroup of G.
        # This requires G to be a group and G_Y to be a group.
        q = is_group(G) and is_group(G_Y)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Y is a subset of X",
    "¬Q: G_{Y} is not a subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1