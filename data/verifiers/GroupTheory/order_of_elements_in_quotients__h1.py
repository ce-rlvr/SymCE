import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_normal(N, G):
    try:
        if hasattr(N, 'is_normal'):
            return N.is_normal(G)
    except Exception:
        pass
    try:
        for gen in N.generators:
            if gen not in G:
                return False
        for g in G.generators:
            try:
                g_inv = ~g
            except Exception:
                g_inv = g.inv()
            for n in N.generators:
                if (g * n * g_inv) not in N:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, N, g = witness
            try:
                n = g.order()
            except Exception:
                n = -1
        elif len(witness) == 4:
            G, N, g, n = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: N is a normal subgroup of G
    try:
        h1 = is_normal(N, G)
    except Exception:
        h1 = False

    # H2: g is an element of G having finite order n
    try:
        h2 = (g in G) and (g.order() == n) and (n > 0) and (n != float('inf'))
    except Exception:
        h2 = False

    # neg_Q: The order of the coset gN in the quotient group G/N does NOT divide n.
    try:
        k = 1
        curr = g
        # Find order of gN in G/N
        # It is the smallest positive integer k such that g**k in N
        max_k = n + 100 if n > 0 else 1000
        while curr not in N and k <= max_k:
            curr = curr * g
            k += 1
        
        if curr in N:
            neg_q = (n % k != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: g is an element of G having finite order n",
    "¬Q: The order of the coset gN in the quotient group G/N does not divide n"
]

N_HYP = 2
NEG_Q_INDEX = 2