import sympy
import sympy.ntheory
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
    # H_1: G is a finite p-group
    try:
        order = witness.order()
        if order == 1:
            h1_ok = True
            p = 2
        else:
            factors = sympy.ntheory.factorint(order)
            if len(factors) == 1:
                h1_ok = True
                p = list(factors.keys())[0]
            else:
                h1_ok = False
                p = 2
    except Exception:
        h1_ok = False
        p = 2

    # neg_Q: The size of some conjugacy class of G is NOT a power of p
    try:
        neg_q_ok = False
        # To ensure it runs under 5 seconds, we skip computation for very large groups
        if witness.order() <= 5000:
            sizes = []
            if hasattr(witness, 'conjugacy_classes'):
                try:
                    classes = witness.conjugacy_classes()
                    sizes = [len(c) for c in classes]
                    if sum(sizes) != witness.order():
                        sizes = []
                except Exception:
                    sizes = []
            
            if not sizes:
                try:
                    elements = list(witness.elements)
                except Exception:
                    elements = list(witness.generate())
                
                if elements:
                    hashable = True
                    try:
                        hash(elements[0])
                    except Exception:
                        hashable = False
                    
                    if hashable:
                        seen = set()
                        for g in elements:
                            if g not in seen:
                                orbit = set()
                                for h in elements:
                                    try:
                                        h_inv = ~h
                                    except Exception:
                                        h_inv = h**-1
                                    orbit.add(h * g * h_inv)
                                sizes.append(len(orbit))
                                seen.update(orbit)
                    else:
                        seen = []
                        for g in elements:
                            if g not in seen:
                                orbit = []
                                for h in elements:
                                    try:
                                        h_inv = ~h
                                    except Exception:
                                        h_inv = h**-1
                                    conj = h * g * h_inv
                                    if conj not in orbit:
                                        orbit.append(conj)
                                sizes.append(len(orbit))
                                for item in orbit:
                                    if item not in seen:
                                        seen.append(item)
            
            if sizes:
                for size in sizes:
                    if size == 1:
                        continue
                    c_factors = sympy.ntheory.factorint(size)
                    if len(c_factors) > 1 or list(c_factors.keys())[0] != p:
                        neg_q_ok = True
                        break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "¬Q: The size of some conjugacy class of G is not a power of p"
]

N_HYP = 1
NEG_Q_INDEX = 1