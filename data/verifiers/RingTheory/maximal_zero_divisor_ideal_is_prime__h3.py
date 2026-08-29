import sympy
import math

# Top-level setup: named object bindings that the witness expression may reference.
# We provide ZZ and QQ as standard rings. 
# A witness can be:
# 1. An integer `m`, interpreted as the ideal (m) in ZZ.
# 2. A tuple `(ZZ, m)`, interpreted as the ideal (m) in ZZ.
# 3. A tuple `(n, m)`, interpreted as the ring Z/nZ and its ideal (m).
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness):
    try:
        # Unpack witness
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            R = ZZ
            I = witness
            
        # Case 1: R is the ring of integers ZZ
        if R == ZZ:
            m = abs(int(I))
            
            h1 = True  # ZZ is a commutative ring with identity
            h2 = True  # Z = {0} is the set of zero divisors
            
            # H3: For any ideal J strictly containing I, J is not a subset of Z.
            # In ZZ, Z = {0}. The only ideal that is a subset of Z is {0}.
            # Any ideal J strictly containing I=(m) has a generator j dividing m (with j != m).
            # Since j divides m and j != m, j cannot be 0 (unless m=0, but then j>0).
            # Thus J is never {0}, so J is never a subset of Z.
            h3 = True
            
            # neg_Q: I is not a prime ideal
            # In ZZ, (m) is prime iff m is a prime number or m == 0.
            neg_q = not (sympy.isprime(m) or m == 0)
            
            return [h1, h2, h3, neg_q]
            
        # Case 2: R is the field of rationals QQ
        if R == QQ:
            m = abs(int(I))
            
            h1 = True
            h2 = True
            h3 = True
            
            # In a field, the only ideals are (0) and (1).
            if m != 0:
                m = 1
            neg_q = not (m == 0)
            
            return [h1, h2, h3, neg_q]
            
        # Case 3: R is Z/nZ, represented by integer n, and I is (m)
        try:
            n = int(R)
            m = int(I)
            if n == R and m == I:
                if n < 2 or m < 1 or n % m != 0:
                    return [False, False, False, False]
                
                h1 = True  # Z/nZ is a commutative ring with identity
                h2 = True  # Z is the set of zero divisors
                
                # H3: For any ideal J strictly containing I, J is not a subset of Z.
                # J = (j) strictly contains I = (m) iff j | m and j != m.
                # J is a subset of Z iff every element of J is a zero divisor.
                # In Z/nZ, x is a zero divisor iff gcd(x, n) > 1 or x == 0.
                # Thus J is a subset of Z iff gcd(j, n) > 1.
                h3 = True
                for j in range(1, m):
                    if m % j == 0 and n % j == 0:
                        if math.gcd(j, n) > 1:
                            h3 = False
                            break
                            
                # neg_Q: I is not a prime ideal
                # In Z/nZ, (m) is prime iff Z/mZ is an integral domain, which means m is prime.
                neg_q = not sympy.isprime(m)
                
                return [h1, h2, h3, neg_q]
        except Exception:
            pass
            
    except Exception:
        pass
        
    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: Z is the set of all zero divisors of R",
    "H_3: For any ideal J of R strictly containing I, J is not a subset of Z",
    "¬Q: I is not a prime ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3