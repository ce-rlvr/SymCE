import math
import itertools
import functools
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
    n = None
    G = None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, G = witness
        elif hasattr(witness, 'degree') and isinstance(witness, PermutationGroup):
            G = witness
            n = G.degree
        else:
            n_temp = int(witness)
            if n_temp == witness:
                n = n_temp
                G = SymmetricGroup(n)
    except Exception:
        pass

    # H_1: n is an integer
    try:
        h1_ok = (n is not None) and (int(n) == n)
    except Exception:
        h1_ok = False

    # H_2: G is the symmetric group S_n
    try:
        Sn = SymmetricGroup(int(n))
        if G == Sn:
            h2_ok = True
        elif isinstance(G, PermutationGroup) and G.order() == math.factorial(int(n)):
            if G.degree == int(n):
                h2_ok = True
            else:
                h2_ok = G.is_isomorphic(Sn)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The derived length of G is not exactly 3
    try:
        def derived_length(grp):
            curr = grp
            length = 0
            while True:
                if curr.order() == 1:
                    return length
                nxt = curr.derived_subgroup()
                if nxt.order() == curr.order():
                    return float('inf')
                curr = nxt
                length += 1
        
        dl = derived_length(G)
        neg_q_ok = (dl != 3)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "H_2: G is the symmetric group S_n",
    "¬Q: The derived length of G is not exactly 3"
]

N_HYP = 2
NEG_Q_INDEX = 2