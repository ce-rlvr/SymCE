import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H1: N is a normal subgroup of G
    try:
        is_sub = True
        for g in N.generators:
            if g not in G:
                is_sub = False
                break
        
        is_normal = is_sub
        if is_normal:
            for g in G.generators:
                for n in N.generators:
                    conj = g * n * (g**-1)
                    if conj not in N:
                        is_normal = False
                        break
                if not is_normal:
                    break
        h1 = is_normal
    except Exception:
        h1 = False

    # H2: The quotient group G/N is an abelian group
    try:
        is_abelian = True
        for x in G.generators:
            for y in G.generators:
                comm = x * y * (x**-1) * (y**-1)
                if comm not in N:
                    is_abelian = False
                    break
            if not is_abelian:
                break
        h2 = is_abelian
    except Exception:
        h2 = False

    # neg_Q: The commutator subgroup G' is not a subgroup of N
    try:
        D = G.derived_subgroup()
        is_sub_D = True
        for d in D.generators:
            if d not in N:
                is_sub_D = False
                break
        neg_q = not is_sub_D
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: The quotient group G/N is an abelian group",
    "¬Q: The commutator subgroup G' is not a subgroup of N"
]

N_HYP = 2
NEG_Q_INDEX = 2