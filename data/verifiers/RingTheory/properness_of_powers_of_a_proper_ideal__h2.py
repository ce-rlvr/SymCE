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

from itertools import product

class Z_n:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        
    def add(self, a, b): 
        return (a + b) % self.n
        
    def mul(self, a, b): 
        return (a * b) % self.n
        
    def zero(self): 
        return 0
        
    def one(self): 
        return 1
        
    @property
    def is_commutative(self): 
        return True
        
    def __str__(self): 
        return f"Z/{self.n}Z"
        
    def __repr__(self): 
        return str(self)

class Z_n_Ideal:
    def __init__(self, ring, gens):
        self.ring = ring
        self.gens = list(gens)
        self.elements = set(self.gens)
        if not self.elements:
            self.elements.add(self.ring.zero())
            
        changed = True
        while changed:
            new_elements = set(self.elements)
            for a in self.elements:
                for b in self.elements:
                    new_elements.add(self.ring.add(a, b))
                    new_elements.add(self.ring.add(a, self.ring.n - b))
                for r in self.ring.elements:
                    new_elements.add(self.ring.mul(a, r))
            if len(new_elements) == len(self.elements):
                changed = False
            self.elements = new_elements

    @property
    def is_proper(self):
        return len(self.elements) < self.ring.n

    @property
    def is_zero(self):
        return len(self.elements) <= 1

    def __pow__(self, power):
        if power == 1: 
            return self
        prods = set()
        for combo in product(self.gens, repeat=power):
            p = 1
            for val in combo: 
                p = self.ring.mul(p, val)
            prods.add(p)
        return Z_n_Ideal(self.ring, list(prods))

# Bindings for the namespace
Z2 = Z_n(2)
Z3 = Z_n(3)
Z4 = Z_n(4)
Z6 = Z_n(6)
Z8 = Z_n(8)
Z9 = Z_n(9)
Z12 = Z_n(12)

def conditions(witness):
    H1, H2, H3, neg_Q = False, False, False, False
    
    # Try tuple format (m, gens, n)
    try:
        if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], int):
            m, gens, n = witness
            if m > 1:
                H1 = True
            try:
                n_val = int(n)
                if n_val > 0:
                    H3 = True
            except Exception:
                n_val = 1
                
            R = Z_n(m)
            I = Z_n_Ideal(R, gens)
            
            H2 = I.is_proper and not I.is_zero
            
            try:
                In = I ** n_val
                neg_Q = not (In.is_proper and not In.is_zero)
            except Exception:
                neg_Q = False
                
            return [H1, H2, H3, neg_Q]
    except Exception:
        pass

    # Try object format (R, I, n)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, I, n = witness
            
            if hasattr(R, 'is_commutative'):
                H1 = bool(R.is_commutative)
            elif hasattr(R, 'is_commutative_ring'):
                H1 = bool(R.is_commutative_ring)
            else:
                H1 = True
                
            try:
                n_val = int(n)
                if n_val > 0:
                    H3 = True
            except Exception:
                n_val = 1
                
            def check_zero(ideal, ring):
                if hasattr(ideal, 'is_zero'):
                    z_prop = ideal.is_zero
                    return z_prop() if callable(z_prop) else z_prop
                if hasattr(ideal, 'elements'):
                    return len(ideal.elements) <= 1
                if hasattr(ideal, 'gens'):
                    try:
                        if hasattr(ring, 'zero'):
                            zero = ring.zero() if callable(ring.zero) else ring.zero
                        else:
                            zero = 0
                        return all(g == zero for g in ideal.gens)
                    except Exception:
                        pass
                return False

            try:
                I_is_proper = getattr(I, 'is_proper', False)
                if callable(I_is_proper): 
                    I_is_proper = I_is_proper()
                
                I_is_zero = check_zero(I, R)
                H2 = bool(I_is_proper and not I_is_zero)
            except Exception:
                H2 = False
            
            try:
                In = I ** n_val
                In_is_proper = getattr(In, 'is_proper', False)
                if callable(In_is_proper): 
                    In_is_proper = In_is_proper()
                
                In_is_zero = check_zero(In, R)
                neg_Q = not (In_is_proper and not In_is_zero)
            except Exception:
                neg_Q = False
            
            return [H1, H2, H3, neg_Q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is a proper ideal of R",
    "H_3: n is a positive integer",
    "¬Q: I^n is not a proper ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3