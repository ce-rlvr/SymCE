import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            G = witness.get('G')
            R = witness.get('R')
        else:
            n, G, R = witness
    except Exception:
        return [False, False, False]

    # H1: n is an odd positive integer
    try:
        h1 = bool(isinstance(n, (int, sympy.Integer)) and n > 0 and n % 2 == 1)
    except Exception:
        h1 = False

    # H2: G is the dihedral group of order 2n
    try:
        if isinstance(G, PermutationGroup) and h1:
            if G.order() == 2 * n:
                D = DihedralGroup(n)
                h2 = bool(G.is_isomorphic(D))
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: R does NOT constitute exactly one conjugacy class in G
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            try:
                R_set = set(R)
            except TypeError:
                # If R is not iterable, it cannot be a conjugacy class
                neg_q = True
            else:
                G_elements = set(G.elements)
                if not R_set.issubset(G_elements):
                    neg_q = True
                elif not R_set:
                    neg_q = True
                else:
                    r = next(iter(R_set))
                    c_class = set()
                    for g in G_elements:
                        c_class.add(g * r * ~g)
                    
                    is_exact_class = (R_set == c_class)
                    neg_q = not is_exact_class
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an odd positive integer",
    "H_2: G is the dihedral group of order 2n",
    "¬Q: R does not constitute exactly one conjugacy class in G"
]

N_HYP = 2
NEG_Q_INDEX = 2