import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math

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
    # H_1: For every prime p dividing the order of G, there exists a subgroup H of G 
    # such that the index of H in G is coprime to p, and the order of H is coprime to p.
    try:
        order = witness.order()
        primes = sympy.ntheory.primefactors(order)
        h1 = True
        for p in primes:
            # Mathematically, if p divides |G|, and |G| = [G:H] * |H|,
            # p must divide either the index [G:H] or the order |H|.
            # Therefore, it is impossible for BOTH the index and the order to be coprime to p.
            # If there are any prime factors of |G|, this condition is strictly False.
            h1 = False
            break
    except Exception:
        h1 = False

    # ¬Q: G is NOT a solvable group
    try:
        neg_q = not witness.is_solvable
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: For every prime p dividing the order of G, there exists a subgroup H of G such that the index of H in G is coprime to p, and the order of H is coprime to p",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1