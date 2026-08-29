import math
import itertools
import functools
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: A and G are finite groups and C is a conjugacy class of G",
    "H_2: A acts on G by automorphisms",
    "H_3: The orders |A| and |G| are coprime",
    "¬Q: The conjugacy class C contains no element fixed by the action of A"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        A, G, action, C = witness
        C = list(C)
    except Exception:
        return [False, False, False, False]
    
    try:
        elements_A = list(A.elements)
    except Exception:
        try:
            elements_A = list(A.generate())
        except Exception:
            return [False, False, False, False]
            
    try:
        elements_G = list(G.elements)
    except Exception:
        try:
            elements_G = list(G.generate())
        except Exception:
            return [False, False, False, False]

    # H1: A and G are finite groups, C is a conjugacy class of G
    h1 = False
    try:
        if isinstance(A, PermutationGroup) and isinstance(G, PermutationGroup):
            if C:
                c_elem = C[0]
                if c_elem in G:
                    conj_class = set(g * c_elem * (g ** -1) for g in elements_G)
                    if set(C) == conj_class:
                        h1 = True
    except Exception:
        h1 = False

    # H2: A acts on G by automorphisms
    h2 = False
    try:
        is_action = True
        
        for a in elements_A:
            for g in elements_G:
                res = action(a, g)
                if not isinstance(res, Permutation) or res not in G:
                    is_action = False
                    break
            if not is_action: break
            
        if is_action:
            for a in elements_A:
                for g in elements_G:
                    for h in elements_G:
                        if action(a, g * h) != action(a, g) * action(a, h):
                            is_action = False
                            break
                    if not is_action: break
                if not is_action: break
                
        if is_action:
            for a in elements_A:
                for b in elements_A:
                    for g in elements_G:
                        if action(a * b, g) != action(a, action(b, g)):
                            is_action = False
                            break
                    if not is_action: break
                if not is_action: break
                
        if is_action:
            id_A = next(a for a in elements_A if a * a == a)
            for g in elements_G:
                if action(id_A, g) != g:
                    is_action = False
                    break
                    
        h2 = is_action
    except Exception:
        h2 = False

    # H3: The orders |A| and |G| are coprime
    h3 = False
    try:
        if math.gcd(int(A.order()), int(G.order())) == 1:
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: C contains NO element that is fixed by the action of A
    neg_q = False
    try:
        has_fixed = False
        for c in C:
            fixed = True
            for a in elements_A:
                if action(a, c) != c:
                    fixed = False
                    break
            if fixed:
                has_fixed = True
                break
        neg_q = not has_fixed
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]