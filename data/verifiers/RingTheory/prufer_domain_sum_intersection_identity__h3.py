import math
import functools
import sympy

def _lcm(a, b):
    if a == 0 and b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def _gcd_multiple(*args):
    if not args:
        return 0
    return functools.reduce(math.gcd, args)

class Z_Subset:
    """
    Represents either a principal ideal nZ or a finite subset of Z.
    Used to construct witnesses for ring theory conjectures over Z.
    """
    def __init__(self, ideal_gen=None, finite_set=None):
        self.ideal_gen = abs(ideal_gen) if ideal_gen is not None else None
        self.finite_set = frozenset(finite_set) if finite_set is not None else None

    def is_ideal(self):
        return self.ideal_gen is not None and self.finite_set is None

    def is_empty(self):
        return self.ideal_gen is None and self.finite_set is not None and len(self.finite_set) == 0

    def is_zero(self):
        return (self.ideal_gen == 0 and self.finite_set is None) or \
               (self.ideal_gen is None and self.finite_set == frozenset({0}))

    def __add__(self, other):
        if self.is_ideal() and other.is_ideal():
            return Z_Subset(ideal_gen=math.gcd(self.ideal_gen, other.ideal_gen))
        
        ideal = self if self.is_ideal() else (other if other.is_ideal() else None)
        fset = self.finite_set if self.finite_set is not None else (other.finite_set if other.finite_set is not None else None)
        
        if ideal is not None and fset is not None and (self.ideal_gen is None or other.ideal_gen is None):
            if ideal.ideal_gen == 0:
                return Z_Subset(finite_set=fset)
            rems = frozenset(x % ideal.ideal_gen for x in fset)
            if len(rems) == ideal.ideal_gen:
                return Z_Subset(ideal_gen=1)
            if rems == frozenset({0}):
                return Z_Subset(ideal_gen=ideal.ideal_gen)
            return Z_Subset(ideal_gen=ideal.ideal_gen, finite_set=rems)
            
        if self.finite_set is not None and other.finite_set is not None and self.ideal_gen is None and other.ideal_gen is None:
            return Z_Subset(finite_set={a + b for a in self.finite_set for b in other.finite_set})
            
        raise ValueError("Addition not fully implemented for mixed sets")

    def __and__(self, other):
        if self.is_ideal() and other.is_ideal():
            if self.ideal_gen == 0 and other.ideal_gen == 0:
                return Z_Subset(ideal_gen=0)
            return Z_Subset(ideal_gen=_lcm(self.ideal_gen, other.ideal_gen))
        
        ideal = self if self.is_ideal() else (other if other.is_ideal() else None)
        fset = self.finite_set if self.finite_set is not None else (other.finite_set if other.finite_set is not None else None)
        
        if ideal is not None and fset is not None and (self.ideal_gen is None or other.ideal_gen is None):
            if ideal.ideal_gen == 0:
                return Z_Subset(finite_set=frozenset({0}) if 0 in fset else frozenset())
            return Z_Subset(finite_set={x for x in fset if x % ideal.ideal_gen == 0})
            
        if self.finite_set is not None and other.finite_set is not None and self.ideal_gen is None and other.ideal_gen is None:
            return Z_Subset(finite_set=self.finite_set & other.finite_set)
            
        raise ValueError("Intersection not fully implemented for mixed sets")

    def intersection(self, other):
        return self.__and__(other)

    def __mul__(self, other):
        if self.is_empty() or other.is_empty():
            return Z_Subset(finite_set=frozenset())
        if self.is_zero() or other.is_zero():
            return Z_Subset(finite_set=frozenset({0}))
            
        if self.is_ideal() and other.is_ideal():
            return Z_Subset(ideal_gen=self.ideal_gen * other.ideal_gen)
            
        ideal = self if self.is_ideal() else (other if other.is_ideal() else None)
        fset = self.finite_set if self.finite_set is not None else (other.finite_set if other.finite_set is not None else None)
        
        if ideal is not None and fset is not None and (self.ideal_gen is None or other.ideal_gen is None):
            g = _gcd_multiple(*fset)
            if g == 0:
                return Z_Subset(ideal_gen=0)
            return Z_Subset(ideal_gen=ideal.ideal_gen * g)
            
        if self.finite_set is not None and other.finite_set is not None and self.ideal_gen is None and other.ideal_gen is None:
            return Z_Subset(finite_set={a * b for a in self.finite_set for b in other.finite_set})
            
        raise ValueError("Multiplication not fully implemented for mixed sets")

    def __eq__(self, other):
        if not isinstance(other, Z_Subset):
            return False
        self_ideal = self.ideal_gen
        self_fset = self.finite_set
        if self_ideal == 0 and self_fset is None:
            self_ideal = None
            self_fset = frozenset({0})
            
        other_ideal = other.ideal_gen
        other_fset = other.finite_set
        if other_ideal == 0 and other_fset is None:
            other_ideal = None
            other_fset = frozenset({0})
            
        return self_ideal == other_ideal and self_fset == other_fset

class RingZ_class:
    def is_prufer_domain(self):
        return True
    def is_ideal(self, I):
        return isinstance(I, Z_Subset) and I.is_ideal()

Z = RingZ_class()

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            R, I, J = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a Prüfer domain
    try:
        if hasattr(R, 'is_prufer_domain'):
            h1 = bool(R.is_prufer_domain())
        elif R == sympy.S.Integers:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: I is an ideal of R
    try:
        if hasattr(R, 'is_ideal'):
            h2 = bool(R.is_ideal(I))
        elif hasattr(I, 'is_ideal'):
            h2 = bool(I.is_ideal())
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: (I+J)(I \cap J) != IJ
    try:
        try:
            intersect = I & J
        except Exception:
            intersect = I.intersection(J)
            
        lhs = (I + J) * intersect
        rhs = I * J
        neg_q = not (lhs == rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Prüfer domain",
    "H_2: I is an ideal of R",
    "¬Q: (I+J)(I \\cap J) != IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2