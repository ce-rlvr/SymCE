import sympy
from sympy import S, Set
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup

# Top-level setup: named object bindings for witness expressions
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

Z = S.Integers
N = S.Naturals
R = S.Reals
Q = S.Rationals

def is_group(G):
    if hasattr(G, 'is_group') and G.is_group:
        return True
    if isinstance(G, PermutationGroup):
        return True
    if G in [S.Integers, S.Reals, S.Complexes, S.Rationals]:
        return True
    if isinstance(G, str) and G in ['Z', 'R', 'Q', 'C']:
        return True
    return False

def is_set(X):
    if isinstance(X, Set):
        return True
    if isinstance(X, (int, sympy.Integer)):
        return True
    if hasattr(X, '__len__'):
        return True
    if isinstance(X, str):
        return True
    if X == S.Infinity:
        return True
    return False

def is_infinite(X):
    if X in [S.Integers, S.Reals, S.Complexes, S.Rationals, S.Naturals, S.Naturals0]:
        return True
    if isinstance(X, str) and X in ['Z', 'R', 'Q', 'C', 'N', 'Z+', 'infinite', 'infinity']:
        return True
    if hasattr(X, 'is_finite'):
        if X.is_finite == False:
            return True
    if X == S.Infinity:
        return True
    return False

def is_trivial(A):
    if hasattr(A, 'order'):
        try:
            return A.order() == 1
        except Exception:
            pass
    if A in [S.Integers, S.Reals, S.Complexes, S.Rationals]:
        return False
    if isinstance(A, str) and A in ['Z', 'R', 'Q', 'C']:
        return False
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            X = witness.get('X')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            A, B, X = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: A and B are groups
    try:
        h1 = is_group(A) and is_group(B)
    except Exception:
        h1 = False

    # H_2: B acts on a set X
    try:
        h2 = is_group(B) and is_set(X)
    except Exception:
        h2 = False

    # H_3: A^(X) is the direct sum of copies of A indexed by X
    try:
        h3 = is_group(A) and is_set(X)
    except Exception:
        h3 = False

    # ¬Q: A ≀_X B is not isomorphic to the external semidirect product A^(X) ⋊ B
    # The unrestricted wreath product A ≀_X B is isomorphic to the restricted wreath product A^(X) ⋊ B
    # if and only if X is finite or A is trivial. Thus, the conclusion fails when X is infinite and A is non-trivial.
    try:
        neg_q = is_infinite(X) and not is_trivial(A)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A and B are groups",
    "H_2: B acts on a set X",
    "H_3: A^(X) is the direct sum of copies of A indexed by X",
    "¬Q: A ≀_X B is not isomorphic to the external semidirect product A^(X) ⋊ B"
]

N_HYP = 3
NEG_Q_INDEX = 3