import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        elif hasattr(witness, 'domain') and hasattr(witness, 'codomain'):
            G = witness.domain
            H = witness.codomain
        else:
            return [False, False]
            
        # H_1: G is a divisible group
        try:
            # For finite groups, a group is divisible if and only if it is the trivial group.
            # Proof: Let |G| = m. For any x in G, x^m = e. If G is divisible, for any g in G,
            # there exists x such that x^m = g. Thus g = e. So G is trivial.
            h1 = hasattr(G, 'order') and G.order() == 1
        except Exception:
            h1 = False
            
        # neg_Q: H is NOT a divisible group
        try:
            neg_q = hasattr(H, 'order') and H.order() > 1
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is a divisible group",
    "¬Q: H is not a divisible group"
]

N_HYP = 1
NEG_Q_INDEX = 1