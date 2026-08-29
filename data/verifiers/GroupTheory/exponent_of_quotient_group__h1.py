import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy import eye, zeros
from sympy import lcm

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

def get_exponent(G):
    if hasattr(G, 'elements'):
        e = 1
        for g in G.elements:
            e = lcm(e, g.order())
        return e
    else:
        raise ValueError("G must have .elements")

def is_normal_subgroup(G, N):
    if not isinstance(N, PermutationGroup) or not isinstance(G, PermutationGroup):
        return False
    if not N.is_subgroup(G):
        return False
    for n in N.generators:
        for g in G.generators:
            if (g * n * ~g) not in N:
                return False
            if (~g * n * g) not in N:
                return False
    return True

def get_quotient_exponent(G, N):
    exp_GN = 1
    for g in G.elements:
        k = 1
        curr = g
        max_k = G.order()
        while curr not in N and k <= max_k:
            curr = curr * g
            k += 1
        if k > max_k:
            raise ValueError("Infinite order or not a subgroup")
        exp_GN = lcm(exp_GN, k)
    return exp_GN

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, N, e = witness
            elif len(witness) == 2:
                G, N = witness
                e = get_exponent(G)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        # H1: N is a normal subgroup of G
        try:
            h1 = is_normal_subgroup(G, N)
        except Exception:
            h1 = False
            
        # H2: G has a finite exponent e
        try:
            if int(e) > 0:
                actual_e = get_exponent(G)
                h2 = (int(e) == int(actual_e))
            else:
                h2 = False
        except Exception:
            h2 = False
            
        # neg_Q: The exponent of G/N does NOT divide e
        try:
            exp_GN = get_quotient_exponent(G, N)
            neg_q = (int(e) % int(exp_GN) != 0)
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: G has a finite exponent e",
    "¬Q: The exponent of the quotient group G/N does not divide e"
]

N_HYP = 2
NEG_Q_INDEX = 2