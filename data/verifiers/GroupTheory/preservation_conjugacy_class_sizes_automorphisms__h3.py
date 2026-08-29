import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        if len(witness) == 3:
            G, phi, x = witness
        elif len(witness) == 2:
            G, phi = witness
            x = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: G is a finite group
    h1 = False
    elements = []
    try:
        if hasattr(G, 'is_group') and G.is_group:
            elements = list(G.elements)
            h1 = True
        elif isinstance(G, PermutationGroup):
            elements = list(G.elements)
            h1 = True
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
            h1 = True
        elif isinstance(G, (list, set, tuple)):
            elements = list(G)
            h1 = True
            for a in elements:
                for b in elements:
                    if a * b not in elements:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: phi is an automorphism of G
    h2 = False
    phi_func = None
    try:
        if h1:
            if isinstance(phi, dict):
                phi_func = lambda g: phi.get(g, None)
            else:
                phi_func = phi
            
            mapped_elements = []
            h2 = True
            for g in elements:
                mg = phi_func(g)
                if mg not in elements:
                    h2 = False
                    break
                mapped_elements.append(mg)
            
            if h2:
                if len(set(mapped_elements)) != len(elements):
                    h2 = False
                else:
                    for g in elements:
                        for h in elements:
                            if phi_func(g * h) != phi_func(g) * phi_func(h):
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False

    # neg_Q: The cardinality of the conjugacy class of x in G is not equal to the cardinality of the conjugacy class of phi(x) in G
    neg_q = False
    try:
        if h1 and phi_func is not None:
            def conj_class_size(target):
                s = set()
                for h in elements:
                    try:
                        inv_h = ~h
                    except Exception:
                        inv_h = h**-1
                    s.add(h * target * inv_h)
                return len(s)
            
            if x is not None:
                if x in elements:
                    cx_size = conj_class_size(x)
                    cphix_size = conj_class_size(phi_func(x))
                    neg_q = cx_size != cphix_size
            else:
                for g in elements:
                    if conj_class_size(g) != conj_class_size(phi_func(g)):
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: phi is an automorphism of G",
    "¬Q: The cardinality of the conjugacy class of x in G is not equal to the cardinality of the conjugacy class of phi(x) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2