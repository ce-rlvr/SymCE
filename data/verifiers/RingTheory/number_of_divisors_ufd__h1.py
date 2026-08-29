import math
import sympy
from sympy.abc import x, y, z

# Expected witness format for the ring Z/nZ:
# witness = (n, a, u, factors)
# where:
#   n (int): the modulus of the ring Z/nZ (n >= 2)
#   a (int): the element in Z/nZ
#   u (int): a unit in Z/nZ
#   factors (list of tuples): prime factorization of a, as a list of (p_i, e_i)
#
# Example counterexample: witness = (6, 4, 1, [(2, 2)])

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 4:
            return [False, False, False]
            
        n, a, u, factors = witness
        
        if not isinstance(n, int) or n < 2:
            return [False, False, False]
            
        if not isinstance(a, int) or not isinstance(u, int):
            return [False, False, False]
            
        if not isinstance(factors, (list, tuple)):
            return [False, False, False]
            
        # H_1: a is a non-zero, non-unit element of R
        try:
            is_nonzero = (a % n) != 0
            is_nonunit = math.gcd(a % n, n) != 1
            h1 = is_nonzero and is_nonunit
        except Exception:
            h1 = False
            
        # H_2: a = u p_1^{e_1} ... p_k^{e_k} is the prime factorization of a
        try:
            u_is_unit = math.gcd(u % n, n) == 1
            
            primes_ok = True
            for p, e in factors:
                if not isinstance(p, int) or not isinstance(e, int):
                    primes_ok = False
                    break
                if e < 1:
                    primes_ok = False
                    break
                # In Z/nZ, p is a prime element iff gcd(p, n) is a prime number
                if not sympy.isprime(math.gcd(p % n, n)):
                    primes_ok = False
                    break
                    
            pairwise_ok = True
            for i in range(len(factors)):
                for j in range(i + 1, len(factors)):
                    p1 = factors[i][0]
                    p2 = factors[j][0]
                    # In Z/nZ, two elements are associates iff their gcd with n are equal
                    if math.gcd(p1 % n, n) == math.gcd(p2 % n, n):
                        pairwise_ok = False
                        break
                        
            prod = u % n
            for p, e in factors:
                prod = (prod * pow(p, e, n)) % n
            prod_ok = (prod == a % n)
            
            h2 = u_is_unit and primes_ok and pairwise_ok and prod_ok
        except Exception:
            h2 = False
            
        # ¬Q: The number of non-associate divisors of a is NOT exactly (e_1 + 1)...(e_k + 1)
        try:
            # In Z/nZ, the number of non-associate divisors of a is exactly 
            # the number of integer divisors of gcd(a, n)
            g = math.gcd(a % n, n)
            num_divisors = 0
            for i in range(1, g + 1):
                if g % i == 0:
                    num_divisors += 1
                    
            expected = 1
            for p, e in factors:
                expected *= (e + 1)
                
            neg_q = (num_divisors != expected)
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: a is a non-zero, non-unit element of R",
    "H_2: a = u p_1^{e_1} ... p_k^{e_k} is a valid prime factorization",
    "¬Q: The number of non-associate divisors of a is NOT exactly (e_1 + 1)...(e_k + 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2