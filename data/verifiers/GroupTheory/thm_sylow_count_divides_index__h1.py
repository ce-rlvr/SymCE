import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime, factorint
import math

# Top-level setup
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

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness is expected to be a tuple: (G, p, n_p, P)
    or (G, p) from which n_p and P can be derived.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                G, p, n_p, P = witness
            elif len(witness) == 2:
                G, p = witness
                P = G.sylow_subgroup(p)
                S_elems = set(P.generate())
                orbit = set()
                for g in G.generate():
                    conj_elems = frozenset({g * x * (g**-1) for x in S_elems})
                    orbit.add(conj_elems)
                n_p = len(orbit)
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: n_p is the number of Sylow p-subgroups of G
    try:
        if hasattr(G, 'sylow_subgroup_count'):
            actual_n_p = G.sylow_subgroup_count(p)
        elif hasattr(G, 'sylow_subgroups'):
            actual_n_p = len(G.sylow_subgroups(p))
        else:
            actual_P = G.sylow_subgroup(p)
            S_elems = set(actual_P.generate())
            orbit = set()
            for g in G.generate():
                conj_elems = frozenset({g * x * (g**-1) for x in S_elems})
                orbit.add(conj_elems)
            actual_n_p = len(orbit)
        h2 = bool(n_p == actual_n_p)
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        if hasattr(P, 'is_sylow_p_subgroup'):
            h3 = bool(P.is_sylow_p_subgroup(G, p))
        elif hasattr(G, 'is_sylow_p_subgroup'):
            h3 = bool(G.is_sylow_p_subgroup(P, p))
        else:
            is_sub = P.is_subgroup(G)
            order_G = G.order()
            order_P = P.order()
            k = factorint(order_G).get(p, 0)
            h3 = bool(is_sub and order_P == p**k)
    except Exception:
        h3 = False

    # ¬Q: n_p does not divide the index of P in G
    try:
        order_G = G.order()
        order_P = P.order()
        if order_G == float('inf') or order_G == sympy.oo:
            if order_P != float('inf') and order_P != sympy.oo:
                neg_q = True
            else:
                neg_q = False
        elif order_G % order_P != 0:
            neg_q = True
        else:
            index = order_G // order_P
            neg_q = bool(index % n_p != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: n_p is the number of Sylow p-subgroups of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: n_p does not divide the index of P in G"
]

N_HYP = 3
NEG_Q_INDEX = 3