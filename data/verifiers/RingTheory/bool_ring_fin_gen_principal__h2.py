import itertools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# --- Top-level setup ---

class CofiniteRingElement:
    """
    Represents an element in the Boolean ring of finite and cofinite subsets of N.
    is_cofinite: bool, True if the set is cofinite, False if finite.
    exceptions: frozenset of integers. If finite, these are the elements.
                If cofinite, these are the elements NOT in the set.
    """
    def __init__(self, is_cofinite, exceptions):
        self.is_cofinite = bool(is_cofinite)
        self.exceptions = frozenset(exceptions)
    
    def __add__(self, other):
        # Symmetric difference
        return CofiniteRingElement(
            self.is_cofinite ^ other.is_cofinite,
            self.exceptions ^ other.exceptions
        )
    
    def __mul__(self, other):
        # Intersection
        if not self.is_cofinite and not other.is_cofinite:
            return CofiniteRingElement(False, self.exceptions & other.exceptions)
        elif self.is_cofinite and not other.is_cofinite:
            return CofiniteRingElement(False, other.exceptions - self.exceptions)
        elif not self.is_cofinite and other.is_cofinite:
            return CofiniteRingElement(False, self.exceptions - other.exceptions)
        else:
            return CofiniteRingElement(True, self.exceptions | other.exceptions)
            
    def __eq__(self, other):
        if not isinstance(other, CofiniteRingElement):
            return False
        return self.is_cofinite == other.is_cofinite and self.exceptions == other.exceptions

    def __hash__(self):
        return hash((self.is_cofinite, self.exceptions))

class CofiniteRing:
    def __init__(self):
        self.zero = CofiniteRingElement(False, frozenset())
        self.one = CofiniteRingElement(True, frozenset())
        
    def add(self, a, b):
        return a + b
        
    def mul(self, a, b):
        return a * b
        
    def eq(self, a, b):
        return a == b
        
    def sample(self, n):
        samples = [self.zero, self.one]
        for i in range(n):
            samples.append(CofiniteRingElement(False, frozenset([i, i+1])))
            samples.append(CofiniteRingElement(True, frozenset([i])))
        return samples[:n]

class FiniteSubsetsIdeal:
    def __init__(self, ring):
        self.ring = ring
        
    def contains(self, x):
        return isinstance(x, CofiniteRingElement) and not x.is_cofinite
        
    def sample(self, n):
        samples = [self.ring.zero]
        for i in range(n):
            samples.append(CofiniteRingElement(False, frozenset([i, i*2])))
        return samples[:n]
        
    def not_principal_witness(self, g):
        # Returns an element x in the ideal such that x is not a multiple of g
        if not isinstance(g, CofiniteRingElement) or g.is_cofinite:
            return self.ring.zero
        m = 0
        while m in g.exceptions:
            m += 1
        return CofiniteRingElement(False, frozenset([m]))

# Named object bindings for the witness expression to reference
BooleanRingOfSubsets = CofiniteRing()
IdealOfFiniteSubsets = FiniteSubsetsIdeal(BooleanRingOfSubsets)


def conditions(witness) -> list[bool]:
    try:
        R, I = witness
    except Exception:
        return [False, False]
        
    try:
        # H_1: R is a Boolean ring
        if hasattr(R, 'sample'):
            samples = R.sample(15)
        else:
            samples = []
            
        if hasattr(R, 'zero'):
            R_zero = R.zero
        else:
            R_zero = None
            
        is_boolean_ring = True
        if not samples or R_zero is None:
            is_boolean_ring = False
        else:
            if R_zero not in samples:
                samples.append(R_zero)
                
            for a in samples:
                if not R.eq(R.add(a, R_zero), a):
                    is_boolean_ring = False
                if not R.eq(R.add(a, a), R_zero):
                    is_boolean_ring = False
                if not R.eq(R.mul(a, a), a):
                    is_boolean_ring = False
                for b in samples:
                    if not R.eq(R.add(a, b), R.add(b, a)):
                        is_boolean_ring = False
                    if not R.eq(R.mul(a, b), R.mul(b, a)):
                        is_boolean_ring = False
                    for c in samples:
                        ab_c = R.mul(R.mul(a, b), c)
                        a_bc = R.mul(a, R.mul(b, c))
                        if not R.eq(ab_c, a_bc):
                            is_boolean_ring = False
                            
                        ab_plus_c = R.add(R.add(a, b), c)
                        a_plus_bc = R.add(a, R.add(b, c))
                        if not R.eq(ab_plus_c, a_plus_bc):
                            is_boolean_ring = False
                        
                        a_b_plus_c = R.mul(a, R.add(b, c))
                        ab_plus_ac = R.add(R.mul(a, b), R.mul(a, c))
                        if not R.eq(a_b_plus_c, ab_plus_ac):
                            is_boolean_ring = False
    except Exception:
        is_boolean_ring = False

    try:
        # neg_Q: I is an ideal of R AND I is not a principal ideal
        is_ideal = True
        if not hasattr(I, 'contains') or not hasattr(R, 'zero'):
            is_ideal = False
        elif not I.contains(R.zero):
            is_ideal = False
        else:
            i_samples = I.sample(15) if hasattr(I, 'sample') else []
            r_samples = R.sample(15) if hasattr(R, 'sample') else []
            
            for a in i_samples:
                if not I.contains(a):
                    is_ideal = False
                for b in i_samples:
                    if not I.contains(R.add(a, b)):
                        is_ideal = False
                for r in r_samples:
                    if not I.contains(R.mul(a, r)):
                        is_ideal = False
                        
        is_not_principal = True
        if not hasattr(I, 'sample') or not hasattr(R, 'eq') or not hasattr(R, 'mul'):
            is_not_principal = False
        else:
            i_samples = I.sample(15)
            if not i_samples:
                is_not_principal = False
            else:
                for g in i_samples:
                    if hasattr(I, 'not_principal_witness'):
                        x = I.not_principal_witness(g)
                    else:
                        x = R.zero
                    if not I.contains(x):
                        is_not_principal = False
                    if R.eq(R.mul(x, g), x):
                        is_not_principal = False
                        
        neg_q = is_ideal and is_not_principal
    except Exception:
        neg_q = False

    return [is_boolean_ring, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: I is an ideal of R and I is not a principal ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1