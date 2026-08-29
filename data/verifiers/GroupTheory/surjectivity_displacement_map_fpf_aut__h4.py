import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: \\phi is an automorphism of G",
    "H_3: For all g \\in G, \\phi(g) = g implies g = e",
    "¬Q: The map f is not a bijection"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, phi = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G.generate())
        h1 = len(elements) > 0
    except Exception:
        h1 = False

    # H_2: \phi is an automorphism of G
    try:
        if not h1:
            raise ValueError
        mapped = []
        for g in elements:
            val = phi(g) if callable(phi) else phi[g]
            mapped.append(val)
            
        is_bijection = True
        for i in range(len(mapped)):
            for j in range(i + 1, len(mapped)):
                if mapped[i] == mapped[j]:
                    is_bijection = False
                    break
            if not is_bijection:
                break
                
        if not is_bijection:
            h2 = False
        else:
            h2 = True
            for g in elements:
                for h in elements:
                    val_g = phi(g) if callable(phi) else phi[g]
                    val_h = phi(h) if callable(phi) else phi[h]
                    val_gh = phi(g * h) if callable(phi) else phi[g * h]
                    if val_gh != val_g * val_h:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: For all g \in G, \phi(g) = g implies g = e
    try:
        if not h1:
            raise ValueError
        h3 = True
        try:
            identity = G.identity
        except Exception:
            identity = elements[0] * (elements[0]**-1)
            
        for g in elements:
            val = phi(g) if callable(phi) else phi[g]
            if val == g and g != identity:
                h3 = False
                break
    except Exception:
        h3 = False

    # ¬Q: The map f is not a bijection
    # The displacement map is defined as f(x) = x^{-1} \phi(x)
    try:
        if not h1:
            raise ValueError
        f_values = []
        for g in elements:
            val = phi(g) if callable(phi) else phi[g]
            f_val = (g**-1) * val
            f_values.append(f_val)
            
        is_bijection = True
        for i in range(len(f_values)):
            for j in range(i + 1, len(f_values)):
                if f_values[i] == f_values[j]:
                    is_bijection = False
                    break
            if not is_bijection:
                break
        neg_q = not is_bijection
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]