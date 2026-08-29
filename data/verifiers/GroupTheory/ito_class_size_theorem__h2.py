import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            A = witness.get('A')
            x = witness.get('x')
        else:
            G, A, x = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1_ok = (isinstance(G, PermutationGroup) and 
                 isinstance(A, PermutationGroup) and 
                 all(g in G for g in A.generators) and
                 G.order() % A.order() == 0)
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(x, Permutation) and x in G
    except Exception:
        h2_ok = False

    try:
        orbit = {x}
        queue = [x]
        gens = G.generators
        while queue:
            curr = queue.pop(0)
            for g in gens:
                nxt = g * curr * ~g
                if nxt not in orbit:
                    orbit.add(nxt)
                    queue.append(nxt)
        
        c_size = len(orbit)
        index = G.order() // A.order()
        
        neg_q_ok = (index % c_size != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group and A is a subgroup of G",
    "H_2: x is an element of G",
    "¬Q: The size of the conjugacy class of x in G does not divide the index of A in G"
]

N_HYP = 2
NEG_Q_INDEX = 2