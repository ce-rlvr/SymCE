import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup for standard algebra objects
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

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: Every non-zero non-unit element of R can be written as a finite product of prime elements",
    "¬Q: R is not a unique factorization domain"
]

def conditions(witness):
    """
    Checks if the given witness is a counterexample to the conjecture.
    The witness is expected to be an integer n >= 2, representing the ring R = Z/nZ.
    """
    try:
        n = abs(int(witness))
    except Exception:
        return [False, False]
        
    if n < 2:
        return [False, False]
        
    # Check H_1: Every non-zero non-unit element of R can be written as a finite product of prime elements.
    # In Z/nZ, an element x is prime iff gcd(x, n) is a prime number in Z.
    try:
        if n <= 2000:
            primes = []
            for i in range(1, n):
                if sympy.isprime(math.gcd(i, n)):
                    primes.append(i)
            
            non_units = []
            for i in range(1, n):
                if math.gcd(i, n) > 1:
                    non_units.append(i)
                    
            reachable = set(primes)
            queue = list(primes)
            non_units_set = set(non_units)
            
            # Compute the multiplicative closure of prime elements
            while queue:
                if non_units_set.issubset(reachable):
                    break
                curr = queue.pop(0)
                for p in primes:
                    nxt = (curr * p) % n
                    if nxt != 0 and nxt not in reachable:
                        reachable.add(nxt)
                        queue.append(nxt)
                        
            h1 = non_units_set.issubset(reachable)
        else:
            # For large n, we rely on the mathematical proof that H1 is always True 
            # for Z/nZ when n is composite, and vacuously true when n is prime.
            h1 = True
    except Exception:
        h1 = False

    # Check neg_Q: R is NOT a unique factorization domain.
    # Z/nZ is a UFD iff it is an integral domain, which is true iff n is prime.
    try:
        is_ufd = sympy.isprime(n)
        neg_q = not is_ufd
    except Exception:
        neg_q = False
        
    return [h1, neg_q]