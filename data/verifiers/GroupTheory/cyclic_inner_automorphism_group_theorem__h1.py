import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness) -> list[bool]:
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        Z = witness.center()
        z_order = Z.order()
        g_order = witness.order()
        n = g_order // z_order
        
        h2_ok = False
        if n == 1:
            h2_ok = True
        else:
            z_elements = set(Z.generate_dimino())
            for g in witness.generate_dimino():
                k = 1
                curr = g
                while curr not in z_elements and k <= n:
                    curr = curr * g
                    k += 1
                if k == n:
                    h2_ok = True
                    break
    except Exception:
        h2_ok = False

    try:
        neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Inn(G) is the group of inner automorphisms of G",
    "H_2: Inn(G) is a cyclic group",
    "¬Q: G is not an abelian group or Inn(G) is not the trivial group"
]

N_HYP = 2
NEG_Q_INDEX = 2