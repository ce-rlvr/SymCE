import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Standard algebra objects
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

class CofiniteSet:
    """
    Represents a subset of Integers in the cofinite topology.
    If is_cofinite is False, the set is exactly `elements` (a finite set).
    If is_cofinite is True, the set is Z \ `elements` (a cofinite set).
    
    In the cofinite topology on Z:
    - All subsets are compact.
    - A subset is connected iff it is infinite or has <= 1 elements.
    """
    def __init__(self, elements, is_cofinite=False):
        self.elements = set(elements)
        self.is_cofinite = is_cofinite
        
    def intersect(self, other):
        if not self.is_cofinite and not other.is_cofinite:
            return CofiniteSet(self.elements & other.elements, False)
        elif not self.is_cofinite and other.is_cofinite:
            return CofiniteSet(self.elements - other.elements, False)
        elif self.is_cofinite and not other.is_cofinite:
            return CofiniteSet(other.elements - self.elements, False)
        else:
            return CofiniteSet(self.elements | other.elements, True)
            
    def is_subset(self, other):
        I = self.intersect(other)
        return I.elements == self.elements and I.is_cofinite == self.is_cofinite
        
    @property
    def is_empty(self):
        return not self.is_cofinite and len(self.elements) == 0
        
    @property
    def is_connected(self):
        if self.is_cofinite:
            return True
        return len(self.elements) <= 1
        
    @property
    def is_compact(self):
        return True
        
    def contains(self, x):
        if self.is_cofinite:
            return x not in self.elements
        return x in self.elements

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should provide:
      - witness.C(n): a function returning the n-th set in the sequence
      - witness.intersection: the infinite intersection of the sequence
    """
    try:
        C_func = witness.C
        I = witness.intersection
    except Exception:
        return [False, False, False]
        
    H1_ok = True
    H2_ok = True
    
    try:
        C_prev = None
        for n in range(1, 201):
            Cn = C_func(n)
            
            empty = Cn.is_empty
            if callable(empty): empty = empty()
            if empty:
                H1_ok = False
                
            conn = Cn.is_connected
            if callable(conn): conn = conn()
            if not conn:
                H1_ok = False
                
            if hasattr(Cn, 'is_compact'):
                comp = Cn.is_compact
                if callable(comp): comp = comp()
                if not comp:
                    H1_ok = False
            
            if C_prev is not None:
                if not bool(Cn.is_subset(C_prev)):
                    H2_ok = False
            C_prev = Cn
            
        # Verify the provided intersection
        for n in range(1, 201):
            if not bool(I.is_subset(C_func(n))):
                H1_ok = False
                
        # Elements not in the intersection must be excluded by some C_n
        for x in range(-100, 101):
            if not bool(I.contains(x)):
                excluded = False
                for n in range(1, 501):
                    if not bool(C_func(n).contains(x)):
                        excluded = True
                        break
                if not excluded:
                    H1_ok = False
    except Exception:
        H1_ok = False
        H2_ok = False
        
    try:
        conn_I = I.is_connected
        if callable(conn_I): conn_I = conn_I()
        neg_Q = not bool(conn_I)
    except Exception:
        neg_Q = False
        
    return [H1_ok, H2_ok, neg_Q]

CONDITION_LABELS = [
    "H_1: (C_n) is a sequence of non-empty, compact, connected subsets",
    "H_2: For all n, C_{n+1} is a subset of C_n",
    "¬Q: The intersection is not connected"
]

N_HYP = 2
NEG_Q_INDEX = 2