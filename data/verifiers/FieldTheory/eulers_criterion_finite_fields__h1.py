import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import Matrix, eye, zeros
from sympy.ntheory import isprime
from sympy.polys import Poly
from sympy.abc import x
import itertools

# Top-level setup for standard objects
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: The characteristic of F_q is an odd prime",
    "H_2: a is a non-zero element of F_q",
    "¬Q: a is a square in F_q if and only if a^((q-1)/2) = 1 is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        # Format 1: (p, k, a) where a is a tuple of k integers representing an element in (Z_p)^k
        if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[2], tuple):
            p, k, a = witness
            if not (isprime(p) and p > 2):
                return [False, False, False]
            if not isinstance(k, int) or k < 1:
                return [False, False, False]
            if len(a) != k:
                return [False, False, False]
                
            q = p ** k
            h1 = True
            
            a_mod = tuple(val % p for val in a)
            h2 = any(val != 0 for val in a_mod)
            
            is_sq = True
            for val in a_mod:
                if val == 0:
                    continue
                if pow(val, (p - 1) // 2, p) != 1:
                    is_sq = False
                    break
                    
            power = (q - 1) // 2
            is_pow_1 = True
            for val in a_mod:
                if pow(val, power, p) != 1:
                    is_pow_1 = False
                    break
                    
            neg_q = (is_sq != is_pow_1)
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # Format 2: (q, p, a_coeffs, mod_coeffs) for F_p[x]/(mod_poly)
        elif isinstance(witness, tuple) and len(witness) == 4:
            q, p, a_coeffs, mod_coeffs = witness
            if not (isprime(p) and p > 2):
                return [False, False, False]
                
            a_poly = Poly(a_coeffs, x, modulus=p)
            mod_poly = Poly(mod_coeffs, x, modulus=p)
            
            k = mod_poly.degree()
            if k < 1 or q != p**k:
                return [False, False, False]
                
            h1 = True
            h2 = not (a_poly % mod_poly).is_zero
            
            is_sq = False
            for coeffs in itertools.product(range(p), repeat=k):
                mat_poly = Poly(coeffs, x, modulus=p)
                if (mat_poly**2 % mod_poly) == (a_poly % mod_poly):
                    is_sq = True
                    break
                    
            power = (q - 1) // 2
            res = Poly(1, x, modulus=p)
            base = a_poly % mod_poly
            while power > 0:
                if power % 2 == 1:
                    res = (res * base) % mod_poly
                base = (base * base) % mod_poly
                power //= 2
                
            is_pow_1 = (res == Poly(1, x, modulus=p))
            
            neg_q = (is_sq != is_pow_1)
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # Format 3: (q, p, a) where a is an integer (Z_q ring)
        elif isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[2], int):
            q, p, a = witness
            if not (isprime(p) and p > 2):
                return [False, False, False]
            if q != p:
                return [False, False, False]
                
            h1 = True
            h2 = (a % p != 0)
            
            is_sq = False
            for val in range(q):
                if (val * val) % q == a % q:
                    is_sq = True
                    break
                    
            is_pow_1 = (pow(a, (q - 1) // 2, q) == 1)
            neg_q = (is_sq != is_pow_1)
            return [bool(h1), bool(h2), bool(neg_q)]
            
    except Exception:
        pass
        
    return [False, False, False]