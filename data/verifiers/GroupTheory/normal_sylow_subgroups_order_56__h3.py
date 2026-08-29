import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # Extract G and potentially n_2 from the witness
    if isinstance(witness, tuple):
        G = witness[0]
    else:
        G = witness

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: The order of G is 56
    try:
        h2_ok = h1_ok and G.order() == 56
    except Exception:
        h2_ok = False

    # H_3: n_2 is the number of Sylow 2-subgroups of G
    try:
        if not h2_ok:
            h3_ok = False
        else:
            if isinstance(witness, tuple) and len(witness) >= 2:
                n_2_wit = witness[1]
                P2 = G.sylow_subgroup(2)
                P2_elems = list(P2.generate())
                sylow2_sets = set()
                for g in G.generate():
                    conj = frozenset([~g * x * g for x in P2_elems])
                    sylow2_sets.add(conj)
                actual_n_2 = len(sylow2_sets)
                h3_ok = (n_2_wit == actual_n_2)
            else:
                h3_ok = True
    except Exception:
        h3_ok = False

    # ¬Q: Either n_7 = 1 or n_2 = 1 (Negation: n_7 != 1 and n_2 != 1)
    try:
        if not h2_ok:
            neg_q = False
        else:
            # Compute actual n_2
            P2 = G.sylow_subgroup(2)
            P2_elems = list(P2.generate())
            sylow2_sets = set()
            for g in G.generate():
                conj = frozenset([~g * x * g for x in P2_elems])
                sylow2_sets.add(conj)
            actual_n_2 = len(sylow2_sets)

            # Compute actual n_7
            P7 = G.sylow_subgroup(7)
            P7_elems = list(P7.generate())
            sylow7_sets = set()
            for g in G.generate():
                conj = frozenset([~g * x * g for x in P7_elems])
                sylow7_sets.add(conj)
            actual_n_7 = len(sylow7_sets)

            neg_q = (actual_n_7 != 1) and (actual_n_2 != 1)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is 56",
    "H_3: n_2 is the number of Sylow 2-subgroups of G",
    "¬Q: n_7 != 1 and n_2 != 1"
]

N_HYP = 3
NEG_Q_INDEX = 3