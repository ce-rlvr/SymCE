import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
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
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class MockGroup:
    """
    A mock group class to represent infinite groups like (Q, +) or (R, +)
    which are not natively available in SymPy's combinatorics module.
    """
    def __init__(self, name, is_group=True, is_fg=True):
        self.name = name
        self.is_group = is_group
        self.is_finitely_generated = is_fg
        self.normal_subgroups = []

    def add_normal_subgroup(self, N):
        self.normal_subgroups.append(N)

    def is_normal(self, N):
        return N in self.normal_subgroups

    def __repr__(self):
        return self.name

# Standard counterexamples for the Finitely Generated Extension Theorem
Q_plus = MockGroup("Q_plus", is_group=True, is_fg=False)
trivial_Q = MockGroup("trivial_Q", is_group=True, is_fg=True)
Q_plus.add_normal_subgroup(trivial_Q)

R_plus = MockGroup("R_plus", is_group=True, is_fg=False)
trivial_R = MockGroup("trivial_R", is_group=True, is_fg=True)
R_plus.add_normal_subgroup(trivial_R)


def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        if hasattr(G, 'is_group'):
            h1 = G.is_group
        elif hasattr(G, 'elements') or hasattr(G, 'generators'):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if hasattr(G, 'is_normal') and callable(G.is_normal):
            try:
                h2 = G.is_normal(N)
            except Exception:
                pass
        if not h2 and hasattr(N, 'is_normal') and callable(N.is_normal):
            try:
                h2 = N.is_normal(G)
            except Exception:
                pass
        if not h2 and hasattr(G, 'normal_subgroups'):
            h2 = N in G.normal_subgroups
    except Exception:
        h2 = False

    # H_3: N is a finitely generated group
    try:
        if hasattr(N, 'is_finitely_generated'):
            h3 = N.is_finitely_generated
        elif hasattr(N, 'elements') or hasattr(N, 'generators'):
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: G is NOT a finitely generated group
    try:
        if hasattr(G, 'is_finitely_generated'):
            neg_q = not G.is_finitely_generated
        elif hasattr(G, 'elements') or hasattr(G, 'generators'):
            neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]


CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a finitely generated group",
    "¬Q: G is not a finitely generated group"
]

N_HYP = 3
NEG_Q_INDEX = 3