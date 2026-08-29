import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G, H, f, S = witness
    except Exception:
        return [False, False, False]
        
    def get_elements(group):
        if hasattr(group, 'generate') and callable(group.generate):
            return list(group.generate())
        elif hasattr(group, 'elements'):
            return list(group.elements)
        else:
            return list(group)

    try:
        G_elements = get_elements(G)
    except Exception:
        return [False, False, False]

    try:
        H_elements = get_elements(H)
    except Exception:
        return [False, False, False]

    if isinstance(f, dict):
        f_eval = lambda x: f[x]
    elif callable(f):
        f_eval = f
    else:
        f_eval = None

    # H_1: f: G -> H is a group homomorphism
    try:
        if f_eval is None:
            h1 = False
        else:
            h1 = True
            for g in G_elements:
                if f_eval(g) not in H_elements:
                    h1 = False
                    break
                    
            if h1:
                for x in G_elements:
                    for y in G_elements:
                        if f_eval(x * y) != f_eval(x) * f_eval(y):
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H_2: S is a subset of G that generates G
    try:
        S_list = list(S)
        if not all(s in G_elements for s in S_list):
            h2 = False
        else:
            if len(S_list) == 0:
                h2 = (len(G_elements) == 1)
            else:
                S_group = PermutationGroup(S_list)
                h2 = (S_group.order() == len(G_elements))
    except Exception:
        h2 = False

    # ¬Q: The image f(S) does NOT generate the image subgroup f(G)
    try:
        if f_eval is None:
            neg_q = False
        else:
            S_list = list(S)
            f_S = list(set([f_eval(s) for s in S_list]))
            f_G = list(set([f_eval(g) for g in G_elements]))
            
            if len(f_S) == 0:
                if len(H_elements) > 0:
                    id_H = H_elements[0]**0
                else:
                    id_H = Permutation()
                f_S_elements = {id_H}
            else:
                f_S_group = PermutationGroup(f_S)
                f_S_elements = set(f_S_group.generate())
                
            f_G_set = set(f_G)
            
            neg_q = (f_S_elements != f_G_set)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: S is a subset of G that generates G",
    "¬Q: <f(S)> != f(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2