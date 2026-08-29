import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint, isprime
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    G, p, q = None, None, None
    
    # Parse witness
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, p, q = witness
        else:
            G = witness
            # Try to infer p and q if only the group is provided
            try:
                order = G.order()
                factors = factorint(order)
                if len(factors) == 2:
                    primes = list(factors.keys())
                    # Find a prime q such that the Sylow q-subgroup is NOT normal
                    for test_q in primes:
                        test_p = primes[0] if primes[1] == test_q else primes[1]
                        S = G.sylow_subgroup(test_q)
                        normal = True
                        for g in G.generators:
                            for h in S.generators:
                                if (g * h * ~g) not in S:
                                    normal = False
                                    break
                            if not normal:
                                break
                        if not normal:
                            p, q = test_p, test_q
                            break
                    # Fallback if both are normal (which means it's not a counterexample)
                    if p is None:
                        p, q = primes[0], primes[1]
            except Exception:
                pass
    except Exception:
        pass

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p and q are distinct primes
    try:
        h2 = bool(isprime(p) and isprime(q) and p != q)
    except Exception:
        h2 = False

    # H_3: The order of G is p^a q^b for positive integers a and b
    try:
        order = G.order()
        factors = factorint(order)
        h3 = bool(len(factors) == 2 and p in factors and q in factors and factors[p] > 0 and factors[q] > 0)
    except Exception:
        h3 = False

    # ¬Q: The Sylow q-subgroup of G is not normal in G
    try:
        S = G.sylow_subgroup(q)
        is_norm = True
        for g in G.generators:
            for h in S.generators:
                if (g * h * ~g) not in S:
                    is_norm = False
                    break
            if not is_norm:
                break
        neg_q = not is_norm
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p and q are distinct primes",
    "H_3: The order of G is p^a q^b for positive integers a and b",
    "¬Q: The Sylow q-subgroup of G is not normal in G"
]

N_HYP = 3
NEG_Q_INDEX = 3