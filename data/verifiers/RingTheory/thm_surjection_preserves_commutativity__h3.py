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
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class ModInt:
    """A simple class for integers modulo n, useful for constructing finite rings."""
    def __init__(self, val, mod):
        self.val = val % mod
        self.mod = mod
    def __add__(self, other):
        return ModInt(self.val + other.val, self.mod)
    def __mul__(self, other):
        return ModInt(self.val * other.val, self.mod)
    def __eq__(self, other):
        return isinstance(other, ModInt) and self.val == other.val and self.mod == other.mod
    def __hash__(self):
        return hash((self.val, self.mod))
    def __repr__(self):
        return f"{self.val} mod {self.mod}"

class ModMatrix:
    """A simple class for matrices over integers modulo n, useful for constructing finite rings."""
    def __init__(self, mat, mod):
        self.mat = Matrix(mat).applyfunc(lambda x: x % mod)
        self.mod = mod
    def __add__(self, other):
        return ModMatrix(self.mat + other.mat, self.mod)
    def __mul__(self, other):
        return ModMatrix(self.mat * other.mat, self.mod)
    def __eq__(self, other):
        return isinstance(other, ModMatrix) and self.mat == other.mat and self.mod == other.mod
    def __hash__(self):
        return hash((tuple(self.mat), self.mod))
    def __repr__(self):
        return f"{self.mat} mod {self.mod}"

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, S, f) where:
      - R is a list/set of elements forming the domain ring.
      - S is a list/set of elements forming the codomain ring.
      - f is a dictionary, list of pairs, or callable representing the homomorphism.
    """
    try:
        R, S, f = witness
    except Exception:
        return [False, False, False, False]

    def apply_f(func, x):
        if isinstance(func, dict):
            return func[x]
        elif isinstance(func, list):
            for k, v in func:
                if k == x:
                    return v
            raise ValueError("Mapping not found")
        return func(x)

    def is_ring(elements):
        if not hasattr(elements, '__len__') or len(elements) > 1000:
            return False
        if not elements:
            return False
        try:
            elements = list(elements)
        except Exception:
            return False
            
        # Closure
        for a in elements:
            for b in elements:
                if (a + b) not in elements: return False
                if (a * b) not in elements: return False
                
        # Associativity and distributivity
        for a in elements:
            for b in elements:
                ab_plus = a + b
                ab_mul = a * b
                for c in elements:
                    if ab_plus + c != a + (b + c): return False
                    if ab_mul * c != a * (b * c): return False
                    if a * (b + c) != ab_mul + (a * c): return False
                    if ab_plus * c != (a * c) + (b * c): return False
                    
        # Commutativity of addition
        for a in elements:
            for b in elements:
                if a + b != b + a: return False
                
        # Additive identity (zero)
        zeros_list = [z for z in elements if all(z + a == a for a in elements)]
        if not zeros_list: return False
        zero = zeros_list[0]
        
        # Additive inverses
        for a in elements:
            if not any(a + b == zero for b in elements): return False
            
        # Multiplicative identity (one)
        ones_list = [e for e in elements if all(e * a == a and a * e == a for a in elements)]
        if not ones_list: return False
        
        return True

    def is_homomorphism(domain, codomain, mapping):
        if not hasattr(domain, '__len__') or len(domain) > 1000: return False
        if not hasattr(codomain, '__len__') or len(codomain) > 1000: return False
        
        # Well-defined mapping into codomain
        for a in domain:
            try:
                fa = apply_f(mapping, a)
            except Exception:
                return False
            if fa not in codomain: return False
            
        # Preserves addition and multiplication
        for a in domain:
            try:
                fa = apply_f(mapping, a)
            except Exception:
                return False
            for b in domain:
                try:
                    fb = apply_f(mapping, b)
                    if apply_f(mapping, a + b) != fa + fb: return False
                    if apply_f(mapping, a * b) != fa * fb: return False
                except Exception:
                    return False
                    
        # Preserves multiplicative identity
        ones_R = [e for e in domain if all(e * a == a and a * e == a for a in domain)]
        ones_S = [e for e in codomain if all(e * a == a and a * e == a for a in codomain)]
        if not ones_R or not ones_S: return False
        try:
            if apply_f(mapping, ones_R[0]) != ones_S[0]: return False
        except Exception:
            return False
            
        return True

    def is_commutative(elements):
        if not hasattr(elements, '__len__') or len(elements) > 1000:
            return False
        try:
            elements = list(elements)
        except Exception:
            return False
        for a in elements:
            for b in elements:
                if a * b != b * a: return False
        return True

    # H_1: R and S are rings
    try:
        h1 = is_ring(R) and is_ring(S)
    except Exception:
        h1 = False

    # H_2: f is a ring homomorphism from R to S
    try:
        h2 = is_homomorphism(R, S, f)
    except Exception:
        h2 = False

    # H_3: R is a commutative ring
    try:
        h3 = is_commutative(R)
    except Exception:
        h3 = False

    # ¬Q: S is not a commutative ring
    try:
        neg_q = not is_commutative(S)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a ring homomorphism from R to S",
    "H_3: R is a commutative ring",
    "¬Q: S is not a commutative ring"
]

N_HYP = 3
NEG_Q_INDEX = 3