import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard group bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard matrix bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _unpack(witness):
    """
    Flexibly unpack the witness which could be (P, p), (P, X, p), or (P, p, X).
    Returns (P, p, degree) where degree is the size of the set X.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                P, p = witness
                degree = P.degree if hasattr(P, 'degree') else 0
                return P, p, degree
            elif len(witness) == 3:
                if isinstance(witness[2], int) and not isinstance(witness[1], int):
                    P, X, p = witness
                elif isinstance(witness[1], int) and not isinstance(witness[2], int):
                    P, p, X = witness
                else:
                    P, X, p = witness
                
                if isinstance(X, int):
                    degree = X
                elif hasattr(X, '__len__'):
                    degree = len(X)
                else:
                    degree = P.degree if hasattr(P, 'degree') else 0
                
                p_degree = P.degree if hasattr(P, 'degree') else 0
                degree = max(degree, p_degree)
                return P, p, degree
    except Exception:
        pass
    return None, None, None

def conditions(witness):
    P, p, degree = _unpack(witness)
    
    if P is None:
        return [False, False, False, False]

    # H_1: P is a finite p-group
    try:
        if not isinstance(P, PermutationGroup):
            h1_ok = False
        elif not isinstance(p, int) or p < 2:
            h1_ok = False
        else:
            order = P.order()
            if order == 1:
                h1_ok = True
            else:
                temp = order
                while temp % p == 0:
                    temp //= p
                h1_ok = (temp == 1)
    except Exception:
        h1_ok = False

    # H_2: X is a finite set
    try:
        h2_ok = isinstance(P, PermutationGroup) and isinstance(degree, int) and degree >= 0
    except Exception:
        h2_ok = False

    # H_3: X^P is the set of elements in X fixed by all elements of P
    try:
        h3_ok = isinstance(P, PermutationGroup)
    except Exception:
        h3_ok = False

    # ¬Q: |X| \not\equiv |X^P| \pmod p
    try:
        if not isinstance(P, PermutationGroup) or not isinstance(p, int) or p < 2:
            neg_q_ok = False
        else:
            fixed_points = 0
            for i in range(degree):
                if i < P.degree:
                    if all(g(i) == i for g in P.generators):
                        fixed_points += 1
                else:
                    # Points beyond P.degree are fixed by definition
                    fixed_points += 1
            
            neg_q_ok = (degree % p) != (fixed_points % p)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is a finite p-group",
    "H_2: X is a finite set",
    "H_3: X^P is the set of elements in X fixed by all elements of P",
    "¬Q: |X| is not congruent to |X^P| modulo p"
]

N_HYP = 3
NEG_Q_INDEX = 3