import sympy
from sympy import abc

class Z_Ideal:
    def __init__(self, gen):
        self.gen = abs(int(gen))
        
    def __pow__(self, n):
        if n == 0:
            return Z_Ideal(1)
        if n < 0:
            raise ValueError("Negative power")
        return Z_Ideal(self.gen ** n)
        
    def is_subset(self, other):
        if type(other) is not Z_Ideal:
            return False
        if other.gen == 0:
            return self.gen == 0
        return self.gen % other.gen == 0
        
    def is_maximal(self):
        return sympy.isprime(self.gen)
        
    def is_prime(self):
        return self.gen == 0 or sympy.isprime(self.gen)
        
    def __eq__(self, other):
        if type(other) is not Z_Ideal:
            return False
        return self.gen == other.gen
        
    def __repr__(self):
        return f"Z_Ideal({self.gen})"

class Zm_Ideal:
    def __init__(self, m, gen):
        self.m = abs(int(m))
        self.gen = sympy.gcd(int(gen), self.m)
        
    def __pow__(self, n):
        if n == 0:
            return Zm_Ideal(self.m, 1)
        if n < 0:
            raise ValueError("Negative power")
        return Zm_Ideal(self.m, self.gen ** n)
        
    def is_subset(self, other):
        if type(other) is not Zm_Ideal or self.m != other.m:
            return False
        return self.gen % other.gen == 0
        
    def is_maximal(self):
        if self.m <= 1: 
            return False
        if self.gen == self.m:
            return sympy.isprime(self.m)
        return sympy.isprime(self.m // self.gen)
        
    def is_prime(self):
        return self.is_maximal()
        
    def __eq__(self, other):
        if type(other) is not Zm_Ideal or self.m != other.m:
            return False
        return self.gen == other.gen
        
    def __repr__(self):
        return f"Zm_Ideal({self.m}, {self.gen})"

class PolyIdeal:
    def __init__(self, gen, gens=None):
        if isinstance(gen, sympy.Poly):
            self.gen = gen.set_domain('QQ')
        else:
            self.gen = sympy.Poly(gen, gens, domain='QQ')
            
    def __pow__(self, n):
        if n == 0:
            return PolyIdeal(1, self.gen.gens)
        if n < 0:
            raise ValueError("Negative power")
        return PolyIdeal(self.gen ** n)
        
    def is_subset(self, other):
        if type(other) is not PolyIdeal:
            return False
        if other.gen.is_zero:
            return self.gen.is_zero
        q, r = sympy.div(self.gen, other.gen)
        return r.is_zero
        
    def is_maximal(self):
        if self.gen.is_zero or self.gen.is_constant():
            return False
        return self.gen.is_irreducible
        
    def is_prime(self):
        if self.gen.is_zero:
            return True
        if self.gen.is_constant():
            return False
        return self.gen.is_irreducible
        
    def __eq__(self, other):
        if type(other) is not PolyIdeal:
            return False
        if self.gen.is_zero:
            return other.gen.is_zero
        if other.gen.is_zero:
            return False
        q, r = sympy.div(self.gen, other.gen)
        q2, r2 = sympy.div(other.gen, self.gen)
        return r.is_zero and r2.is_zero
        
    def __repr__(self):
        return f"PolyIdeal({self.gen})"

# Top-level setup bindings
Z = "Z"
Qx = "Q[x]"

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                R, M, P, n = witness
            elif len(witness) == 3:
                M, P, n = witness
                R = None
            else:
                return [False, False, False, False]
        elif isinstance(witness, dict):
            M = witness['M']
            P = witness['P']
            n = witness['n']
            R = witness.get('R', None)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    if type(M) is int:
        M = Z_Ideal(M)
    if type(P) is int:
        P = Z_Ideal(P)

    if type(M) not in (Z_Ideal, Zm_Ideal, PolyIdeal):
        return [False, False, False, False]
    if type(P) not in (Z_Ideal, Zm_Ideal, PolyIdeal):
        return [False, False, False, False]
    if not isinstance(n, (int, sympy.Integer)):
        return [False, False, False, False]
    
    n = int(n)

    try:
        # The ideal classes provided are all from commutative rings with identity
        h1 = True
    except Exception:
        h1 = False

    try:
        h2 = bool(M.is_maximal())
    except Exception:
        h2 = False

    try:
        p_is_prime = bool(P.is_prime())
        Mn = M ** n
        is_sub = bool(Mn.is_subset(P))
        h3 = p_is_prime and is_sub
    except Exception:
        h3 = False

    try:
        neg_q = not (P == M)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M is a maximal ideal of R",
    "H_3: P is a prime ideal of R such that M^n is a subset of P",
    "¬Q: P is not equal to M"
]

N_HYP = 3
NEG_Q_INDEX = 3