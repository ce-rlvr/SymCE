import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from math import lcm

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
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, N, e = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            if N.is_subgroup(G):
                is_normal = True
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * (~g)) not in N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h2 = is_normal
    except Exception:
        h2 = False

    # neg_Q: The exponent of the quotient group G/N does not divide e
    try:
        e_val = int(e)
        if h1 and h2:
            exp = 1
            for g in G.elements:
                k = 1
                curr = g
                while curr not in N:
                    curr = curr * g
                    k += 1
                exp = lcm(exp, k)
            neg_q = (e_val % exp != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The exponent of the quotient group G/N does not divide e"
]

N_HYP = 2
NEG_Q_INDEX = 2