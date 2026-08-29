import math
import itertools
import functools
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, p = witness
        else:
            R, p = "2z", witness
            
        R_str = str(R).replace(" ", "").lower()
        
        if R_str.endswith("z") and not R_str.startswith("z_") and not R_str.startswith("z/"):
            n_str = R_str[:-1]
            if n_str == "":
                n = 1
            elif n_str == "-":
                n = 1
            else:
                n = int(n_str)
            
            n = abs(n)
            
            if n >= 2:
                try:
                    p = int(p)
                except Exception:
                    return [False, False]
                
                if p % n != 0:
                    return [False, False]
                
                h1 = (p != 0)
                
                def divides(p, x):
                    if p == 0: return x == 0
                    return x % (p * n) == 0

                is_prime_elem = True
                for a_mult in range(-30, 31):
                    for b_mult in range(-30, 31):
                        a = a_mult * n
                        b = b_mult * n
                        if divides(p, a * b):
                            if not divides(p, a) and not divides(p, b):
                                is_prime_elem = False
                                break
                    if not is_prime_elem:
                        break

                is_prime_ideal = (abs(p) != n)
                if is_prime_ideal:
                    for a_mult in range(-30, 31):
                        for b_mult in range(-30, 31):
                            a = a_mult * n
                            b = b_mult * n
                            if (a * b) % p == 0:
                                if a % p != 0 and b % p != 0:
                                    is_prime_ideal = False
                                    break
                        if not is_prime_ideal:
                            break

                neg_q = (is_prime_elem != is_prime_ideal)
                return [h1, neg_q]
            elif n == 1:
                try:
                    p = int(p)
                except Exception:
                    return [False, False]
                h1 = (p != 0)
                return [h1, False]
                
        if R_str.startswith("z_") or R_str.startswith("z/"):
            n_str = "".join(c for c in R_str if c.isdigit())
            if n_str:
                n = int(n_str)
                if n >= 2:
                    try:
                        p = int(p) % n
                    except Exception:
                        return [False, False]
                    
                    h1 = (p != 0)
                    
                    def divides_zn(p, x):
                        g = math.gcd(p, n)
                        return x % g == 0
                    
                    is_unit = math.gcd(p, n) == 1
                    
                    is_zero_divisor = False
                    for i in range(1, n):
                        if (p * i) % n == 0:
                            is_zero_divisor = True
                            break
                            
                    is_prime_elem = not is_unit and not is_zero_divisor
                    if is_prime_elem:
                        for a in range(n):
                            for b in range(n):
                                if divides_zn(p, (a * b) % n):
                                    if not divides_zn(p, a) and not divides_zn(p, b):
                                        is_prime_elem = False
                                        break
                            if not is_prime_elem:
                                break
                                
                    g = math.gcd(p, n)
                    is_prime_ideal = (g != 1)
                    if is_prime_ideal:
                        for a in range(n):
                            for b in range(n):
                                if (a * b) % g == 0:
                                    if a % g != 0 and b % g != 0:
                                        is_prime_ideal = False
                                        break
                            if not is_prime_ideal:
                                break
                                
                    neg_q = (is_prime_elem != is_prime_ideal)
                    return [h1, neg_q]

        # Fallback
        try:
            p = int(p)
            h1 = (p != 0)
            return [h1, False]
        except Exception:
            return [False, False]
            
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: p is a non-zero element of R",
    "¬Q: The element p is a prime element if and only if the principal ideal generated by p is a prime ideal is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1