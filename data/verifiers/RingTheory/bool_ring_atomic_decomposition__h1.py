import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol

# Standard group theory and linear algebra objects
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

# Standard ring theory objects for the witness
class ZRing:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
    def add(self, a, b):
        return (a + b) % self.n
    def mul(self, a, b):
        return (a * b) % self.n
    def __str__(self):
        return f"ZRing({self.n})"
    def __eq__(self, other):
        return isinstance(other, ZRing) and self.n == other.n
    def __hash__(self):
        return hash(self.n)

class BooleanRing:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(1 << n))
        self.zero = 0
    def add(self, a, b):
        return a ^ b
    def mul(self, a, b):
        return a & b
    def __str__(self):
        return f"BooleanRing({self.n})"
    def __eq__(self, other):
        return isinstance(other, BooleanRing) and self.n == other.n
    def __hash__(self):
        return hash(self.n)

class ProductRing:
    def __init__(self, R1, R2):
        self.R1 = R1
        self.R2 = R2
        self.elements = [(a, b) for a in R1.elements for b in R2.elements]
        self.zero = (R1.zero, R2.zero)
    def add(self, a, b):
        return (self.R1.add(a[0], b[0]), self.R2.add(a[1], b[1]))
    def mul(self, a, b):
        return (self.R1.mul(a[0], b[0]), self.R2.mul(a[1], b[1]))
    def __str__(self):
        return f"ProductRing({self.R1}, {self.R2})"

def parse_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        R, x = witness
        if isinstance(R, int):
            R = ZRing(R)
        return R, x
    return None, None

def is_atom(a, R, elements):
    if a == R.zero:
        return False
    # In ring theory, an atom (especially in the context of orthogonal decompositions)
    # is a primitive idempotent.
    if R.mul(a, a) != a:
        return False
    for y in elements:
        if R.mul(y, y) == y:
            if R.mul(y, a) == y and R.mul(a, y) == y:
                if y != R.zero and y != a:
                    return False
    return True

def is_sum_of_orthogonal_atoms(x, R, elements):
    atoms = [a for a in elements if is_atom(a, R, elements)]
    for r in range(len(atoms) + 1):
        for subset in itertools.combinations(atoms, r):
            orthogonal = True
            for i in range(len(subset)):
                for j in range(i + 1, len(subset)):
                    if R.mul(subset[i], subset[j]) != R.zero or R.mul(subset[j], subset[i]) != R.zero:
                        orthogonal = False
                        break
                if not orthogonal:
                    break
            if orthogonal:
                s = R.zero
                for a in subset:
                    s = R.add(s, a)
                if s == x:
                    return True
    return False

def conditions(witness):
    R, x = parse_witness(witness)
    if R is None or x is None:
        return [False, False]
    
    try:
        elements = list(R.elements)
    except Exception:
        return [False, False]
        
    try:
        h1 = (x in elements) and (x != R.zero)
    except Exception:
        h1 = False
        
    try:
        q = is_sum_of_orthogonal_atoms(x, R, elements)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a non-zero element of R",
    "¬Q: x cannot be expressed as a sum of mutually orthogonal atoms of R"
]

N_HYP = 1
NEG_Q_INDEX = 1