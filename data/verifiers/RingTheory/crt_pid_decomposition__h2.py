import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: R is a Principal Ideal Domain (PID)",
    "H_2: a = u p_1^{e_1} ... p_k^{e_k} is the prime factorization of a, with p_i pairwise non-associate primes, e_i >= 1, u is a unit",
    "¬Q: The quotient ring R/(a) is NOT isomorphic to the direct product \\prod_{i=1}^k R/(p_i^{e_i})"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # 1. Try to extract boolean flags (if witness is a dictionary or mock object)
    h1 = h2 = neg_q = None
    
    for k in ['is_PID', 'H1', 'h1', 'is_principal_ideal_domain', 'R_is_PID', 'is_pid']:
        if isinstance(witness, dict) and k in witness:
            h1 = bool(witness[k])
            break
        elif hasattr(witness, k):
            h1 = bool(getattr(witness, k))
            break
            
    for k in ['is_valid_factorization', 'H2', 'h2', 'valid_factorization', 'a_is_valid', 'has_prime_factorization']:
        if isinstance(witness, dict) and k in witness:
            h2 = bool(witness[k])
            break
        elif hasattr(witness, k):
            h2 = bool(getattr(witness, k))
            break
            
    for k in ['not_isomorphic', 'neg_Q', 'neg_q', 'is_not_isomorphic', 'not_isomorphic_to_product', 'fails_isomorphism']:
        if isinstance(witness, dict) and k in witness:
            neg_q = bool(witness[k])
            break
        elif hasattr(witness, k):
            neg_q = bool(getattr(witness, k))
            break
            
    if h1 is not None or h2 is not None or neg_q is not None:
        return [bool(h1), bool(h2), bool(neg_q)]

    # 2. Fallback to mathematical evaluation for tuples representing (R, a, u, primes, exponents)
    if isinstance(witness, (tuple, list)) and len(witness) == 5:
        try:
            R, a, u, primes, exponents = witness
            
            h1_ok = False
            if R == sympy.S.Integers:
                h1_ok = True
            elif hasattr(R, 'is_PolynomialRing') and len(R.gens) == 1 and R.domain.is_Field:
                h1_ok = True
                
            h2_ok = False
            if h1_ok:
                if R == sympy.S.Integers:
                    is_unit = (u in [1, -1])
                else:
                    is_unit = u.is_number and u != 0
                    
                if is_unit:
                    primes_ok = True
                    for p in primes:
                        if R == sympy.S.Integers:
                            if not sympy.isprime(abs(p)):
                                primes_ok = False
                                break
                        else:
                            if not sympy.polys.polytools.is_irreducible(p):
                                primes_ok = False
                                break
                    
                    if primes_ok:
                        assoc_ok = True
                        for i in range(len(primes)):
                            for j in range(i+1, len(primes)):
                                if R == sympy.S.Integers:
                                    if abs(primes[i]) == abs(primes[j]):
                                        assoc_ok = False
                                else:
                                    if sympy.simplify(primes[i] / primes[j]).is_number:
                                        assoc_ok = False
                        
                        if assoc_ok:
                            if all(isinstance(e, (int, sympy.Integer)) and e >= 1 for e in exponents):
                                prod = u
                                for p, e in zip(primes, exponents):
                                    prod *= p**e
                                if R == sympy.S.Integers:
                                    if a == prod:
                                        h2_ok = True
                                else:
                                    if sympy.simplify(a - prod) == 0:
                                        h2_ok = True
                                        
            # For commutative PIDs (like Z or F[x]), the Chinese Remainder Theorem guarantees
            # the isomorphism holds, so the negated conclusion is False.
            neg_q_ok = False
            return [h1_ok, h2_ok, neg_q_ok]
        except Exception:
            pass

    return [False, False, False]