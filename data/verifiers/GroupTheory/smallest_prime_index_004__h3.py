import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import primefactors
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
    # Extract G, H, p from the witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            p = witness.get('p')
            # Auto-fill p if missing but G is provided
            if p is None and G is not None:
                try:
                    factors = primefactors(G.order())
                    if factors:
                        p = min(factors)
                except Exception:
                    pass
        else:
            if len(witness) == 3:
                G, H, p = witness
            elif len(witness) == 2:
                G, H = witness
                p = None
                try:
                    factors = primefactors(G.order())
                    if factors:
                        p = min(factors)
                except Exception:
                    pass
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: p is the smallest prime number dividing the order of G
    try:
        factors = primefactors(G.order())
        h2_ok = (len(factors) > 0) and (p == min(factors))
    except Exception:
        h2_ok = False

    # ¬Q: H is not a normal subgroup of G
    try:
        if not isinstance(H, PermutationGroup):
            neg_q_ok = False
        elif not H.is_subgroup(G):
            neg_q_ok = True
        else:
            neg_q_ok = not G.is_normal(H)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is the smallest prime number dividing the order of G",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2