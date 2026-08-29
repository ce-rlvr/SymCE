import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

class MockRing:
    """
    A mock ring object to represent standard counterexamples 
    that are difficult to construct natively in SymPy.
    """
    def __init__(self, name, is_domain, accp, ufd):
        self.name = name
        self._is_domain = is_domain
        self._accp = accp
        self._ufd = ufd

    @property
    def is_integral_domain(self):
        return self._is_domain

    @property
    def satisfies_ACCP(self):
        return self._accp

    @property
    def is_UFD(self):
        return self._ufd

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

# Standard counterexamples for this conjecture
Z_sqrt_minus_5 = MockRing("Z[sqrt(-5)]", True, True, False)
R_X_Y_Z_W_mod_XY_ZW = MockRing("R[X,Y,Z,W]/(XY-ZW)", True, True, False)
Z_x = MockRing("Z[x]", True, True, True)


def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    """
    # H1: R is an integral domain
    try:
        if hasattr(witness, 'is_integral_domain'):
            h1 = witness.is_integral_domain
            if callable(h1): h1 = h1()
        elif hasattr(witness, 'is_IntegralDomain'):
            h1 = witness.is_IntegralDomain
            if callable(h1): h1 = h1()
        elif hasattr(witness, 'get_ring') and hasattr(witness, 'get_field'):
            # SymPy domains are integral domains
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: R satisfies the ascending chain condition on principal ideals (ACCP)
    try:
        if hasattr(witness, 'satisfies_ACCP'):
            h2 = witness.satisfies_ACCP
            if callable(h2): h2 = h2()
        elif hasattr(witness, 'is_Noetherian'):
            h2 = witness.is_Noetherian
            if callable(h2): h2 = h2()
        elif hasattr(witness, 'get_ring') and hasattr(witness, 'get_field'):
            # Standard SymPy domains (ZZ, QQ, and their poly rings) are Noetherian, hence satisfy ACCP
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: R is NOT a unique factorization domain
    try:
        if hasattr(witness, 'is_UFD'):
            is_ufd = witness.is_UFD
            if callable(is_ufd): is_ufd = is_ufd()
        elif hasattr(witness, 'is_ufd'):
            is_ufd = witness.is_ufd
            if callable(is_ufd): is_ufd = is_ufd()
        else:
            # Default to True so neg_Q is False if we cannot determine
            is_ufd = True
            
        neg_q = not bool(is_ufd)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: R satisfies the ascending chain condition on principal ideals (ACCP)",
    "¬Q: R is not a unique factorization domain"
]

N_HYP = 2
NEG_Q_INDEX = 2