import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime
import math

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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
        else:
            if isinstance(witness[0], int):
                p, G = witness
            else:
                G, p = witness
    except Exception:
        return [False, False]

    try:
        h1 = bool(isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    try:
        expected = math.factorial(p - 2)
        if G.order() % p != 0:
            actual = 1
        else:
            P = G.sylow_subgroup(p)
            P_elements = set(P.elements)
            conjugates = set()
            for g in G.elements:
                H_elements = frozenset({g * x * ~g for x in P_elements})
                conjugates.add(H_elements)
            actual = len(conjugates)
        neg_q = bool(actual != expected)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "¬Q: The number of Sylow p-subgroups of G is not exactly (p-2)!"
]

N_HYP = 1
NEG_Q_INDEX = 1