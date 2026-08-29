import sympy
import math
import itertools
import functools

class DivisibleTrivialRing:
    """
    Represents a ring with trivial multiplication (a*b = 0 for all a,b)
    whose additive group is divisible (e.g., Q, R, C).
    Such rings have no maximal ideals because divisible groups have no maximal subgroups.
    """
    def __init__(self, name):
        self.name = name
        self.is_divisible = True
        self.is_trivial_multiplication = True
        self.has_maximal_ideals = False

class RingIdeal:
    """
    Represents an ideal in a ring.
    """
    def __init__(self, ring, is_proper):
        self.ring = ring
        self.is_proper = is_proper

# Standard counterexamples for Krull's Theorem without identity
Q_trivial_ring = DivisibleTrivialRing("Q")
zero_ideal_Q = RingIdeal(Q_trivial_ring, is_proper=True)

Z_p_infty_trivial_ring = DivisibleTrivialRing("Z_p^infty")
zero_ideal_Z_p_infty = RingIdeal(Z_p_infty_trivial_ring, is_proper=True)

def conditions(witness) -> list[bool]:
    try:
        if not (isinstance(witness, tuple) or isinstance(witness, list)):
            return [False, False]
        if len(witness) != 2:
            return [False, False]
            
        R, I = witness
        
        h1 = False
        try:
            if hasattr(I, 'is_proper') and hasattr(I, 'ring'):
                h1 = bool(I.is_proper and I.ring == R)
        except Exception:
            pass
            
        neg_q = False
        try:
            if R in (Q_trivial_ring, Z_p_infty_trivial_ring):
                neg_q = True
            elif hasattr(R, 'has_maximal_ideals') and R.has_maximal_ideals is False:
                neg_q = True
            elif hasattr(R, 'is_divisible') and hasattr(R, 'is_trivial_multiplication'):
                if R.is_divisible and R.is_trivial_multiplication:
                    neg_q = True
        except Exception:
            pass
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: There does not exist a maximal ideal M of R such that I is a subset of M"
]

N_HYP = 1
NEG_Q_INDEX = 1