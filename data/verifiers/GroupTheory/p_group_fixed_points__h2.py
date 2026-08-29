import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            G = witness.get('G')
        elif isinstance(witness, (list, tuple)) and len(witness) >= 2:
            p = witness[0]
            G = witness[1]
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: X is a finite set
    try:
        h2 = hasattr(G, 'degree') and isinstance(G.degree, (int, sympy.Integer)) and G.degree >= 0
    except Exception:
        h2 = False

    # H_3: G acts on X
    try:
        h3 = isinstance(G, PermutationGroup)
    except Exception:
        h3 = False

    # H_4: X^G is the set of all elements in X fixed by every element of G
    # This is definitional and satisfied by our evaluation strategy if H_2 and H_3 hold.
    try:
        h4 = bool(h2 and h3)
    except Exception:
        h4 = False

    # ¬Q: |X^G| is not congruent to |X| modulo p
    try:
        if h1 and h2 and h3:
            fixed_points = 0
            for i in range(G.degree):
                if all(g(i) == i for g in G.generators):
                    fixed_points += 1
            neg_q = (fixed_points % p) != (G.degree % p)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: X is a finite set",
    "H_3: G acts on X",
    "H_4: X^G is the set of all elements in X fixed by every element of G",
    "¬Q: |X^G| is not congruent to |X| modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4