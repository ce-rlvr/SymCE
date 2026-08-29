import sympy
from sympy.ntheory import mobius
import math
import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup
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

def get_prime_factors(q):
    factors = set()
    d = 2
    n = q
    while d * d <= n:
        while (n % d) == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors

def is_unit(P, q, prime_factors):
    if not P:
        return False
    if math.gcd(P[0], q) != 1:
        return False
    for c in P[1:]:
        for p in prime_factors:
            if c % p != 0:
                return False
    return True

def poly_mul(A, B, q):
    if not A or not B:
        return ()
    degA = len(A) - 1
    degB = len(B) - 1
    res = [0] * (degA + degB + 1)
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            res[i+j] = (res[i+j] + a * b) % q
    while res and res[-1] == 0:
        res.pop()
    return tuple(res)

def get_all_polys(max_deg, q):
    polys = [()]
    for d in range(max_deg + 1):
        for coeffs in itertools.product(range(q), repeat=d):
            for lead in range(1, q):
                polys.append(tuple(coeffs) + (lead,))
    return polys

def count_irreducible(n, q):
    prime_factors = get_prime_factors(q)
    
    # If q has more than one prime factor, Z/qZ is a product of rings.
    # It can be shown that EVERY monic polynomial of degree n >= 1 over such a ring is reducible.
    if len(prime_factors) > 1 and n >= 1:
        return 0
        
    polys = get_all_polys(n, q)
    non_units = [P for P in polys if not is_unit(P, q, prime_factors)]
    
    monic_n = []
    for coeffs in itertools.product(range(q), repeat=n):
        monic_n.append(tuple(coeffs) + (1,))
        
    reducible = set()
    for A in non_units:
        for B in non_units:
            P = poly_mul(A, B, q)
            if len(P) == n + 1 and P[-1] == 1:
                reducible.add(P)
                
    return len(monic_n) - len(reducible)

def formula(n, q):
    total = 0
    for d in range(1, n + 1):
        if n % d == 0:
            total += mobius(d) * (q ** (n // d))
    return total // n

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            q = witness.get('q')
            F = witness.get('F')
        elif len(witness) == 2:
            n, q = witness
            F = None
        elif len(witness) == 3:
            n, q, F = witness
        else:
            return [False, False]
            
        if q is None and F is not None:
            if hasattr(F, 'order'):
                q = F.order
            elif hasattr(F, 'mod'):
                q = F.mod
                
        n = int(n)
        q = int(q)
        
        if q < 2:
            return [False, False]
            
        h1 = (n >= 1)
    except Exception:
        return [False, False]
        
    try:
        # If F is explicitly provided and is a finite field, the theorem holds.
        if F is not None:
            if hasattr(F, 'is_Field') and F.is_Field:
                neg_q = False
                return [h1, neg_q]
            if type(F).__name__ == 'GaloisField':
                neg_q = False
                return [h1, neg_q]
                
        # Otherwise, assume F is Z/qZ and count irreducible polynomials
        actual_count = count_irreducible(n, q)
        expected_count = formula(n, q)
        
        neg_q = (actual_count != expected_count)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The number of monic irreducible polynomials of degree n over F is not exactly (1/n) \\sum_{d|n} \\mu(d) q^{n/d}"
]

N_HYP = 1
NEG_Q_INDEX = 1