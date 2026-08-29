import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    else:
        return list(G)

def inv(a):
    try:
        return ~a
    except Exception:
        pass
    try:
        return a**-1
    except Exception:
        pass
    try:
        if callable(a.inv):
            return a.inv()
        return a.inv
    except Exception:
        pass
    raise ValueError("Cannot compute inverse")

def mul(a, b):
    return a * b

def phi(g, x):
    return mul(mul(g, x), inv(g))

def conditions(witness):
    try:
        elements = get_elements(witness)
        if not elements:
            h1 = False
        else:
            h1 = True
            # Check if phi is a homomorphism to Aut(G)
            for g in elements:
                mapped = [phi(g, x) for x in elements]
                for x in elements:
                    if x not in mapped:
                        h1 = False
                        break
                if not h1: break
                
                for x in elements:
                    for y in elements:
                        if phi(g, mul(x, y)) != mul(phi(g, x), phi(g, y)):
                            h1 = False
                            break
                    if not h1: break
                if not h1: break
            
            if h1:
                for g1 in elements:
                    for g2 in elements:
                        for x in elements:
                            if phi(mul(g1, g2), x) != phi(g1, phi(g2, x)):
                                h1 = False
                                break
                        if not h1: break
                    if not h1: break
    except Exception:
        h1 = False

    try:
        elements = get_elements(witness)
        kernel = []
        for g in elements:
            is_in_kernel = True
            for x in elements:
                if phi(g, x) != x:
                    is_in_kernel = False
                    break
            if is_in_kernel:
                kernel.append(g)
                
        center = []
        for g in elements:
            is_in_center = True
            for x in elements:
                if mul(g, x) != mul(x, g):
                    is_in_center = False
                    break
            if is_in_center:
                center.append(g)
                
        neg_q = False
        for k in kernel:
            if k not in center:
                neg_q = True
                break
        if not neg_q:
            for c in center:
                if c not in kernel:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: phi mapping g to gxg^-1 is a homomorphism to Aut(G)",
    "¬Q: The kernel of phi is not the center of G"
]

N_HYP = 1
NEG_Q_INDEX = 1