import math
import itertools
import functools
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    """
    Witness is expected to be a tuple (A, B, n, m) or a dict with these keys.
    Finitely generated abelian groups A and B are represented as lists of integers,
    where each integer k represents a direct summand Z/kZ (and 0 represents Z).
    """
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            n = witness.get('n')
            m = witness.get('m')
        else:
            A, B, n, m = witness
    except Exception:
        return [False, False]

    def is_valid_group(G):
        return isinstance(G, (list, tuple)) and all(type(x) is int and x >= 0 for x in G)

    def is_free_abelian_of_rank(G, r):
        if not is_valid_group(G):
            return False
        if type(r) is not int or r < 0:
            return False
        # Remove trivial summands Z/1Z
        clean = [x for x in G if x != 1]
        # A free abelian group of rank r has exactly r summands, all of which are Z (represented by 0)
        return all(x == 0 for x in clean) and len(clean) == r

    try:
        h1 = is_free_abelian_of_rank(A, n)
    except Exception:
        h1 = False

    try:
        if not is_valid_group(B) or type(m) is not int or m < 0:
            neg_q = False
        elif not is_valid_group(A):
            neg_q = False
        else:
            # The tensor product of Z/aZ and Z/bZ is Z/gcd(a,b)Z.
            # This holds even for free components where a=0 or b=0, since gcd(0, x) = x.
            tensor = []
            for a in A:
                for b in B:
                    tensor.append(math.gcd(a, b))
            
            is_free = is_free_abelian_of_rank(tensor, n * m)
            neg_q = not is_free
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a free abelian group of rank n",
    "¬Q: The tensor product A \\otimes_Z B is not a free abelian group of rank nm"
]

N_HYP = 1
NEG_Q_INDEX = 1