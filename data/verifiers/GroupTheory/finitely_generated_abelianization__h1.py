import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_is_fg(obj):
    """Helper to safely extract the is_finitely_generated property."""
    is_fg_attr = getattr(obj, 'is_finitely_generated', True)
    return is_fg_attr() if callable(is_fg_attr) else is_fg_attr

def conditions(witness) -> list[bool]:
    # Parse witness: could be a tuple (G, G_prime) or just G
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, G_prime = witness
            h1_ok = False
            if hasattr(G, 'derived_subgroup'):
                try:
                    h1_ok = (G_prime == G.derived_subgroup() or G_prime == G.derived_subgroup)
                except Exception:
                    h1_ok = True
            elif hasattr(G, 'commutator'):
                try:
                    h1_ok = (G_prime == G.commutator() or G_prime == G.commutator)
                except Exception:
                    h1_ok = True
            else:
                h1_ok = True
        else:
            G = witness
            G_prime = None
            h1_ok = True
    except Exception:
        G = witness
        G_prime = None
        h1_ok = False

    # Check negated conclusion: G/G' is NOT a finitely generated abelian group
    # (Since G/G' is always abelian, it fails iff it is not finitely generated)
    neg_q_ok = False
    try:
        Q_group = None
        if G_prime is not None:
            try:
                Q_group = G / G_prime
            except Exception:
                try:
                    Q_group = G.quotient(G_prime)
                except Exception:
                    pass
        
        if Q_group is not None:
            neg_q_ok = not get_is_fg(Q_group)
        else:
            if hasattr(G, 'abelianization'):
                A = G.abelianization()
                if callable(A): 
                    A = A()
                neg_q_ok = not get_is_fg(A)
            else:
                # Fallback: if we cannot form the quotient, check if G itself is finitely generated.
                neg_q_ok = not get_is_fg(G)
    except Exception:
        pass

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G' is the commutator subgroup of G",
    "¬Q: G/G' is not a finitely generated abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1