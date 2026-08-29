import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (G, A, a)
    where G is a finite group, A is a subgroup (or subset), and a is an element.
    """
    try:
        G, A, a = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: a is an element of A
    try:
        if hasattr(A, 'contains'):
            h2 = bool(A.contains(a))
        elif hasattr(A, 'elements'):
            h2 = a in A.elements
        else:
            h2 = a in A
    except Exception:
        h2 = False

    # ¬Q: The size of the conjugacy class of a in G does NOT divide the index of A in G
    try:
        if hasattr(A, 'order'):
            A_order = A.order()
        elif hasattr(A, 'elements'):
            A_order = len(set(A.elements))
        else:
            A_order = len(set(A))
            
        if A_order == 0:
            neg_q = False
        else:
            # If the index is not an integer, it doesn't divide in the standard sense
            if G.order() % A_order != 0:
                neg_q = True
            else:
                index = G.order() // A_order
                
                # Compute the size of the conjugacy class of a in G
                conj_class = set()
                for g in G.elements:
                    conj_class.add(g * a * (~g))
                
                c_size = len(conj_class)
                
                if c_size == 0:
                    neg_q = False
                else:
                    neg_q = (index % c_size != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: a is an element of A",
    "¬Q: The size of the conjugacy class of a in G does not divide the index of A in G"
]

N_HYP = 2
NEG_Q_INDEX = 2