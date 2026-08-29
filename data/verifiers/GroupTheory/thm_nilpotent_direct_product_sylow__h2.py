import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness):
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
        if h1:
            order = witness.order()
            h1 = (order > 0 and order != float('inf'))
    except Exception:
        h1 = False

    # neg_Q: G is NOT isomorphic to the direct product of its Sylow subgroups
    # A finite group is isomorphic to the direct product of its Sylow subgroups
    # if and only if every Sylow subgroup is normal in G.
    try:
        if not h1:
            neg_q = False
        else:
            order = witness.order()
            if order == 1:
                neg_q = False
            else:
                primes = factorint(order).keys()
                is_dp = True
                for p in primes:
                    P = witness.sylow_subgroup(p)
                    # Check if P is normal in witness
                    for g in witness.generators:
                        for h in P.generators:
                            conj = g * h * ~g
                            if conj not in P:
                                is_dp = False
                                break
                        if not is_dp:
                            break
                    if not is_dp:
                        break
                neg_q = not is_dp
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G is not isomorphic to the direct product of its Sylow subgroups"
]

N_HYP = 1
NEG_Q_INDEX = 1