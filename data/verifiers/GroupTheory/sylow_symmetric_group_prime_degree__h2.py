import math
import itertools
import functools
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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
    # Witness is expected to be a tuple: (G, p)
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, p = witness
    except Exception:
        return [False, False]

    # H_1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # ¬Q: The number of Sylow p-subgroups of G is not (p-2)!
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            order_G = G.order()
            k = 0
            temp = order_G
            while temp % p == 0 and temp > 0:
                k += 1
                temp //= p
            target_order = p**k
            
            if target_order == 1:
                num_sylow = 1
            else:
                P = G.sylow_subgroup(p)
                
                try:
                    P_els = list(P.elements)
                except AttributeError:
                    P_els = list(P.generate())
                    
                try:
                    G_els = list(G.elements)
                except AttributeError:
                    G_els = list(G.generate())

                conjugates = set()
                for g in G_els:
                    conj = frozenset(g * x * ~g for x in P_els)
                    conjugates.add(conj)
                num_sylow = len(conjugates)
                
            expected = math.factorial(p - 2)
            neg_q_ok = bool(num_sylow != expected)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The number of Sylow p-subgroups of G is not (p-2)!"
]

N_HYP = 1
NEG_Q_INDEX = 1