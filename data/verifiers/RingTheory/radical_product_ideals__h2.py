import math
from functools import reduce
from sympy.ntheory import factorint

# Top-level setup: Object bindings for the witness namespace
class IdealZZ:
    """Represents an ideal in the commutative ring of integers (ZZ)."""
    def __init__(self, gen):
        self.gen = abs(gen)
        
    def __eq__(self, other):
        if isinstance(other, IdealZZ):
            return self.gen == other.gen
        elif isinstance(other, SubsetZZ):
            # An ideal is only equal to a finite subset if both are {0}
            if self.gen == 0 and other.elements == {0}:
                return True
            return False
        return False
        
    def __contains__(self, item):
        if self.gen == 0:
            return item == 0
        return item % self.gen == 0
        
    def intersection(self, other):
        if isinstance(other, IdealZZ):
            return IdealZZ(math.lcm(self.gen, other.gen))
        elif isinstance(other, SubsetZZ):
            return SubsetZZ({x for x in other.elements if x in self})
        return SubsetZZ(set())
        
    def __str__(self):
        return f"IdealZZ({self.gen})"

class SubsetZZ:
    """Represents a generic subset of the commutative ring of integers (ZZ)."""
    def __init__(self, elements):
        self.elements = set(elements)
        
    def __eq__(self, other):
        if isinstance(other, SubsetZZ):
            return self.elements == other.elements
        elif isinstance(other, IdealZZ):
            if other.gen == 0 and self.elements == {0}:
                return True
            return False
        return False
        
    def __contains__(self, item):
        return item in self.elements
        
    def intersection(self, other):
        if isinstance(other, SubsetZZ):
            return SubsetZZ(self.elements.intersection(other.elements))
        elif isinstance(other, IdealZZ):
            return SubsetZZ({x for x in self.elements if x in other})
        return SubsetZZ(set())
        
    def __str__(self):
        return f"SubsetZZ({self.elements})"

def gcd_list(lst):
    if not lst:
        return 0
    return reduce(math.gcd, lst)

def product(I, J):
    """Computes the product ideal IJ."""
    if isinstance(I, IdealZZ) and isinstance(J, IdealZZ):
        return IdealZZ(I.gen * J.gen)
    elif isinstance(I, SubsetZZ) and isinstance(J, IdealZZ):
        gens = [i * J.gen for i in I.elements]
        return IdealZZ(gcd_list(gens))
    elif isinstance(I, IdealZZ) and isinstance(J, SubsetZZ):
        gens = [j * I.gen for j in J.elements]
        return IdealZZ(gcd_list(gens))
    elif isinstance(I, SubsetZZ) and isinstance(J, SubsetZZ):
        gens = [i * j for i in I.elements for j in J.elements]
        return IdealZZ(gcd_list(gens))
    raise ValueError("Invalid types for product")

def rad(X):
    """Computes the radical of an ideal or a subset in ZZ."""
    if isinstance(X, IdealZZ):
        if X.gen == 0:
            return IdealZZ(0)
        factors = factorint(X.gen)
        core = 1
        for p in factors:
            core *= p
        return IdealZZ(core)
    elif isinstance(X, SubsetZZ):
        roots = set()
        for a in X.elements:
            if a == 0:
                roots.add(0)
            elif a == 1:
                roots.update({1, -1})
            elif a == -1:
                roots.add(-1)
            else:
                roots.add(a)
                for n in range(2, abs(a).bit_length() + 2):
                    if n % 2 == 0 and a < 0:
                        continue
                    x = int(round(abs(a)**(1.0/n)))
                    if x**n == abs(a):
                        if a < 0:
                            roots.add(-x)
                        else:
                            roots.add(x)
                            if n % 2 == 0:
                                roots.add(-x)
        return SubsetZZ(roots)
    raise ValueError("Invalid type for rad")

def conditions(witness) -> list[bool]:
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a commutative ring
    try:
        h1 = (R == "ZZ")
    except Exception:
        h1 = False
        
    # H_2: J is an ideal of R
    try:
        h2 = isinstance(J, IdealZZ)
    except Exception:
        h2 = False
        
    # ¬Q: The radical of the product ideal IJ is not equal to \sqrt{I} \cap \sqrt{J}
    try:
        IJ = product(I, J)
        rad_IJ = rad(IJ)
        rad_I = rad(I)
        rad_J = rad(J)
        intersection = rad_I.intersection(rad_J)
        neg_q = not (rad_IJ == intersection)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "¬Q: The radical of the product ideal IJ is not equal to \\sqrt{I} \\cap \\sqrt{J}"
]

N_HYP = 2
NEG_Q_INDEX = 2