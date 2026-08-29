import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Extract G and p from the witness
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            order = G.order()
            p = int(round(order ** (1.0 / 3.0)))
    except Exception:
        G, p = None, None

    # H_1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # H_2: The order of G is p^3
    try:
        h2_ok = bool(G.order() == p**3)
    except Exception:
        h2_ok = False

    # H_3: G is non-abelian
    try:
        h3_ok = bool(not G.is_abelian)
    except Exception:
        h3_ok = False

    # ¬Q: The commutator subgroup G' does NOT have order p OR is NOT equal to the center Z(G)
    try:
        D = G.derived_subgroup()
        Z = G.center()
        
        def is_eq(G1, G2):
            if G1.order() != G2.order():
                return False
            for g in G1.generators:
                if g not in G2:
                    return False
            return True
            
        q_holds = (D.order() == p) and is_eq(D, Z)
        neg_q_ok = not q_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: The order of G is p^3",
    "H_3: G is non-abelian",
    "¬Q: The commutator subgroup G' does not have order p or is not equal to the center Z(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3