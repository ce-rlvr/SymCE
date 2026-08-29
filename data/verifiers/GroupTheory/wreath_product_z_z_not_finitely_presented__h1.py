import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import FreeGroup
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
Z = FreeGroup('x')

def is_trivial(A):
    try:
        if hasattr(A, 'order') and A.order() == 1:
            return True
    except Exception:
        pass
    try:
        if hasattr(A, 'is_trivial') and A.is_trivial:
            return True
    except Exception:
        pass
    try:
        if A == CyclicGroup(1):
            return True
    except Exception:
        pass
    try:
        if isinstance(A, FreeGroup) and len(A.generators) == 0:
            return True
    except Exception:
        pass
    try:
        if isinstance(A, str) and A.lower() in ['trivial', '1', 'e', 'id']:
            return True
    except Exception:
        pass
    try:
        if A == 1:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    # Extract A, B, G from the witness
    if isinstance(witness, dict):
        if 'A' in witness:
            A = witness['A']
            B = witness.get('B', Z)
            G = witness.get('G', Z if is_trivial(A) else f"{A} wr {B}")
        else:
            A = witness
            B = Z
            G = Z if is_trivial(A) else f"{A} wr Z"
    elif isinstance(witness, (tuple, list)) and len(witness) == 3:
        A, B, G = witness
    elif isinstance(witness, (tuple, list)) and len(witness) == 2:
        A, B = witness
        G = Z if is_trivial(A) else f"{A} wr {B}"
    else:
        A = witness
        B = Z
        G = Z if is_trivial(A) else f"{A} wr Z"

    # H1: B is the infinite cyclic group Z
    try:
        h1 = False
        if isinstance(B, FreeGroup) and len(B.generators) == 1:
            h1 = True
        elif B == 'Z' or B == Z:
            h1 = True
    except Exception:
        h1 = False

    # H2: G is the restricted wreath product A \wr B
    try:
        h2 = False
        if is_trivial(A):
            # If A is trivial, A wr B is isomorphic to B
            if G == B or G == 'Z' or G == Z:
                h2 = True
            elif isinstance(G, str) and 'wr' in G:
                h2 = True
        else:
            if isinstance(G, str) and 'wr' in G:
                h2 = True
            elif isinstance(G, (tuple, list)) and G and G[0] == 'wr':
                h2 = True
            elif G == 'A wr B':
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: G is NOT (finitely generated but not finitely presented)
    # Q is True iff G is finitely generated AND not finitely presented.
    # For G = A wr Z, G is finitely generated iff A is finitely generated.
    # G is finitely presented iff A is trivial (since B=Z is infinite).
    try:
        A_is_fg = True
        if is_trivial(A):
            A_is_fg = True
        elif hasattr(A, 'is_finite') and A.is_finite:
            A_is_fg = True
        elif isinstance(A, FreeGroup):
            A_is_fg = True
        elif isinstance(A, str) and ('inf' in A.lower() or 'sum' in A.lower() or 'prod' in A.lower()):
            A_is_fg = False
            
        G_is_fg = A_is_fg
        G_is_fp = is_trivial(A)
        
        q = G_is_fg and (not G_is_fp)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: B is the infinite cyclic group Z",
    "H_2: G is the restricted wreath product A \\wr B",
    "¬Q: G is not finitely generated or G is finitely presented"
]

N_HYP = 2
NEG_Q_INDEX = 2