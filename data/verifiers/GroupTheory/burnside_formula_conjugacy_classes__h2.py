import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # ¬Q: k(G) != 1/|G| * sum_{g \in G} |C_G(g)|
    try:
        if not h1:
            neg_q = False
        else:
            # Get the number of conjugacy classes k(G)
            classes_attr = witness.conjugacy_classes
            if callable(classes_attr):
                k = len(classes_attr())
            else:
                k = len(classes_attr)
                
            # Get the order of the group |G|
            order_attr = witness.order
            if callable(order_attr):
                order = order_attr()
            else:
                order = order_attr
            
            elements = list(witness.generate())
            
            # Calculate sum_{g \in G} |C_G(g)|
            try:
                sum_cent = 0
                for g in elements:
                    cent = witness.centralizer(g)
                    cent_order = cent.order
                    if callable(cent_order):
                        sum_cent += cent_order()
                    else:
                        sum_cent += cent_order
            except Exception:
                # Fallback: |C_G(g)| is the number of elements commuting with g
                sum_cent = sum(1 for x in elements for y in elements if x * y == y * x)
                
            # Check if the conclusion fails (i.e., the formula does not hold)
            neg_q = bool(k * order != sum_cent)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: k(G) != 1/|G| * sum_{g in G} |C_G(g)|"
]

N_HYP = 1
NEG_Q_INDEX = 1