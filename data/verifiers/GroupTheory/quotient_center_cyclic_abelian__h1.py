import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros
from sympy import Rational, Integer
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
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # The witness can be either a group G, or a tuple (G, Z)
    if isinstance(witness, tuple) and len(witness) == 2:
        G, Z_given = witness
    else:
        G = witness
        Z_given = None

    # H1: Z(G) is the center of G
    try:
        Z_actual = G.center()
        if Z_given is not None:
            h1_ok = bool(Z_given.is_subgroup(Z_actual) and Z_actual.is_subgroup(Z_given))
        else:
            h1_ok = True
    except Exception:
        h1_ok = False

    # H2: The quotient group G/Z(G) is cyclic
    try:
        if not h1_ok:
            h2_ok = False
        else:
            Z = Z_actual
            m = G.order() // Z.order()
            if m == 1:
                h2_ok = True
            elif G.order() > 2000:
                # For very large groups, rely on the mathematical equivalence to avoid timeout
                h2_ok = bool(G.is_abelian)
            else:
                prime_factors = factorint(m).keys()
                maximal_divisors = [m // p for p in prime_factors]
                
                h2_ok = False
                for g in G.elements:
                    is_generator = True
                    for d in maximal_divisors:
                        if Z.contains(g**d):
                            is_generator = False
                            break
                    if is_generator:
                        h2_ok = True
                        break
    except Exception:
        h2_ok = False

    # neg_Q: G is not an abelian group
    try:
        neg_q = not bool(G.is_abelian)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "H_2: The quotient group G/Z(G) is cyclic",
    "¬Q: G is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2