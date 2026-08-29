import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, X = witness
        else:
            G = witness
            X = None
            
        try:
            order = G.order()
            h1 = (order > 0 and order < float('inf'))
        except Exception:
            h1 = False
    except Exception:
        h1 = False

    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G.elements)
            
        seen = set()
        classes = []
        
        for g in elements:
            if g not in seen:
                c = set()
                for h in elements:
                    c.add(h * g * (h**-1))
                classes.append(c)
                seen.update(c)
                
        z_g_size = sum(1 for c in classes if len(c) == 1)
        
        if X is not None:
            sum_classes = 0
            for x in X:
                c = set()
                for h in elements:
                    c.add(h * x * (h**-1))
                sum_classes += len(c)
        else:
            sum_classes = sum(len(c) for c in classes)
            
        lhs = len(elements)
        rhs = z_g_size + sum_classes
        
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = ["H_1: G is a finite group", "H_2: G acts on itself by conjugation", "not Q: |G| != |Z(G)| + sum (G : C_G(x_i))"]

N_HYP = 2
NEG_Q_INDEX = 2