import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x')
            A = witness.get('A')
        else:
            G, x, A = witness
            
        if isinstance(x, list):
            x = Permutation(x)
        if isinstance(A, list):
            A = PermutationGroup(A)
    except Exception:
        return [False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: x is an element of G
    try:
        h2 = x in G
    except Exception:
        h2 = False

    # neg_Q: The size of the conjugacy class of x in G does not divide the index of A in G
    try:
        if not isinstance(A, PermutationGroup):
            neg_q = False
        elif not all(g in G for g in A.generators):
            neg_q = False
        else:
            orbit = set()
            queue = [x]
            orbit.add(x)
            gens = G.generators
            while queue:
                curr = queue.pop(0)
                for g in gens:
                    conj = g * curr * (~g)
                    if conj not in orbit:
                        orbit.add(conj)
                        queue.append(conj)
            c_size = len(orbit)
            
            index = G.order() // A.order()
            neg_q = (index % c_size != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is an element of G",
    "¬Q: The size of the conjugacy class of x in G does not divide the index of A in G"
]

N_HYP = 2
NEG_Q_INDEX = 2