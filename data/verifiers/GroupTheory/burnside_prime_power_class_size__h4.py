import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy import isprime
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: G contains a conjugacy class of size p^k",
    "¬Q: G is a simple group"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, p, k = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # H_3: G contains a conjugacy class of size p^k
    try:
        if isinstance(k, (int, sympy.Integer)) and isinstance(p, (int, sympy.Integer)):
            target_size = p**k
            h3 = False
            
            # Try using built-in conjugacy_classes
            if hasattr(G, 'conjugacy_classes'):
                try:
                    classes = G.conjugacy_classes()
                    for c in classes:
                        if hasattr(c, 'size'):
                            size = c.size
                        elif hasattr(c, '__len__'):
                            size = len(c)
                        else:
                            size = len(list(c))
                        if size == target_size:
                            h3 = True
                            break
                except Exception:
                    pass
            
            # Fallback to manual computation if not found or failed
            if not h3 and hasattr(G, 'elements'):
                elements = list(G.elements)
                seen = set()
                for g in elements:
                    if g not in seen:
                        c = set()
                        for h in elements:
                            c.add(h * g * ~h)
                        if len(c) == target_size:
                            h3 = True
                            break
                        seen.update(c)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: G is a simple group (negation of "G is not a simple group")
    try:
        neg_q = None
        if hasattr(G, 'is_simple'):
            try:
                if callable(G.is_simple):
                    is_simple = G.is_simple()
                else:
                    is_simple = G.is_simple
                neg_q = bool(is_simple)
            except Exception:
                pass
        
        if neg_q is None and hasattr(G, 'normal_subgroups'):
            try:
                normal_subgroups = G.normal_subgroups()
                # A simple group has exactly 2 normal subgroups: the trivial group and itself
                neg_q = len(normal_subgroups) == 2
            except Exception:
                pass
                
        if neg_q is None:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]