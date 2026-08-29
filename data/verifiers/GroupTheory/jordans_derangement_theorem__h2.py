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
S1 = SymmetricGroup(1)
S2 = SymmetricGroup(2)
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

def conditions(witness) -> list[bool]:
    # H_1: G is a finite permutation group acting on a set \Omega
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: The action of G on \Omega is transitive
    try:
        h2_ok = bool(witness.is_transitive())
    except Exception:
        h2_ok = False

    # ¬Q: Every element in G has at least one fixed point (no derangement exists)
    try:
        deg = witness.degree
        neg_q_ok = True
        
        # Use generate() for memory efficiency, fallback to elements if unavailable
        try:
            gen = witness.generate()
        except AttributeError:
            gen = witness.elements
            
        for g in gen:
            is_derangement = True
            for i in range(deg):
                if g(i) == i:
                    is_derangement = False
                    break
            
            # If we find a derangement, the conclusion holds, so its negation is False
            if is_derangement:
                neg_q_ok = False
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS: list[str] = [
    "H_1: G is a finite permutation group acting on a set \\Omega",
    "H_2: The action of G on \\Omega is transitive",
    "¬Q: Every element in G has at least one fixed point (no derangement exists)"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2