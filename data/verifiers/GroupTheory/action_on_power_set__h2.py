import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness must provide:
      - G: list of group elements
      - X: list of set elements
      - e: identity element of G
      - mul: callable(g, h) -> g * h
      - inv: callable(g) -> g^-1
      - act: callable(g, x) -> action of g on x
    """
    try:
        G = list(witness.G)
        X = list(witness.X)
        e = witness.e
        mul = witness.mul
        inv = witness.inv
        act = witness.act
    except Exception:
        return [False, False]

    # H1: G is a group acting on a set X
    # This hypothesis is satisfied if G is a valid group and `act` is EITHER a valid left action OR a valid right action.
    try:
        is_group = True
        if e not in G:
            is_group = False
        for g in G:
            if inv(g) not in G:
                is_group = False
            if mul(g, e) != g or mul(e, g) != g:
                is_group = False
            if mul(g, inv(g)) != e or mul(inv(g), g) != e:
                is_group = False
            for h in G:
                if mul(g, h) not in G:
                    is_group = False
                for k in G:
                    if mul(g, mul(h, k)) != mul(mul(g, h), k):
                        is_group = False
                        
        is_left_action = True
        is_right_action = True
        for x in X:
            if act(e, x) != x:
                is_left_action = False
                is_right_action = False
            for g in G:
                if act(g, x) not in X:
                    is_left_action = False
                    is_right_action = False
                for h in G:
                    if act(g, act(h, x)) != act(mul(g, h), x):
                        is_left_action = False
                    if act(g, act(h, x)) != act(mul(h, g), x):
                        is_right_action = False
                        
        h1 = is_group and (is_left_action or is_right_action)
    except Exception:
        h1 = False

    # Conclusion: The mapping g * A = {g * a | a in A} defines a valid group action of G on P(X).
    # The notation g * A implies a LEFT group action. If the underlying action of G on X is a right action 
    # (and G is non-abelian), the induced operation on P(X) fails to satisfy the left action axiom g * (h * A) = (g * h) * A.
    try:
        valid_left_action = True
        for x in X:
            if act(e, x) != x:
                valid_left_action = False
            for g in G:
                if act(g, x) not in X:
                    valid_left_action = False
                for h in G:
                    if act(g, act(h, x)) != act(mul(g, h), x):
                        valid_left_action = False
        neg_q = not valid_left_action
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS: list[str] = [
    "H_1: G is a group acting on a set X",
    "¬Q: The mapping g * A = {g * a | a in A} fails to define a valid left group action on P(X)"
]

N_HYP: int = 1
NEG_Q_INDEX: int = 1