import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
# The witness is expected to be a tuple: (R, a, u, primes, exponents, num_divisors)
# R is a string representing the ring, e.g., 'ZZ'
# a is the element
# u is the unit
# primes is a list of prime elements
# exponents is a list of exponents
# num_divisors is the actual number of non-associate divisors of a in R

def conditions(witness) -> list[bool]:
    try:
        R_str, a, u, primes, exponents, num_divisors = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a unique factorization domain.
    # We only support ZZ and QQ[x] as UFDs for this verification.
    try:
        if R_str == 'ZZ':
            h1 = True
        elif R_str == 'QQ[x]':
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: a = u p_1^{e_1} ... p_k^{e_k} is the prime factorization of a, 
    # where u is a unit, p_i are pairwise non-associate prime elements, and e_i >= 1.
    try:
        if R_str == 'ZZ':
            # Check if u is a unit in ZZ
            if abs(u) != 1:
                h2 = False
            else:
                h2 = True
                prod = u
                seen_primes = set()
                for p, e in zip(primes, exponents):
                    if e < 1:
                        h2 = False
                        break
                    if not sympy.isprime(abs(p)):
                        h2 = False
                        break
                    # Check pairwise non-associate
                    if abs(p) in seen_primes:
                        h2 = False
                        break
                    seen_primes.add(abs(p))
                    prod *= (p ** e)
                if h2 and prod != a:
                    h2 = False
        elif R_str == 'QQ[x]':
            # Check if u is a unit in QQ[x] (i.e., a non-zero rational number)
            if not isinstance(u, (int, Rational, Integer)) or u == 0:
                h2 = False
            else:
                h2 = True
                prod = u
                seen_primes = []
                for p, e in zip(primes, exponents):
                    if e < 1:
                        h2 = False
                        break
                    p_poly = sympy.Poly(p, x, domain='QQ')
                    if not p_poly.is_irreducible:
                        h2 = False
                        break
                    # Check pairwise non-associate
                    # Two polynomials are associate if they differ by a constant factor
                    for sp in seen_primes:
                        q, r = sympy.div(p, sp, domain='QQ')
                        if r == 0 and q.is_number:
                            h2 = False
                            break
                    if not h2:
                        break
                    seen_primes.append(p)
                    prod *= (p ** e)
                if h2 and sympy.simplify(prod - a) != 0:
                    h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The number of non-associate divisors of a in R is NOT exactly the product (e_1 + 1)...(e_k + 1).
    try:
        expected_divisors = 1
        for e in exponents:
            expected_divisors *= (e + 1)
        
        neg_q = (num_divisors != expected_divisors)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a = u p_1^{e_1} ... p_k^{e_k} is the prime factorization of a, with u a unit, p_i pairwise non-associate primes, and e_i >= 1",
    "¬Q: The number of non-associate divisors of a in R is not exactly the product (e_1 + 1)(e_2 + 1) ... (e_k + 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2