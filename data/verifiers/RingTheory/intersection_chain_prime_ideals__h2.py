import math
import sympy
from functools import reduce
from sympy import S
from sympy.abc import x, y, z

Z = S.Integers
Q = S.Rationals

def compute_lcm(args):
    if not args:
        return 1
    def lcm(a, b):
        if a == 0 and b == 0:
            return 0
        return abs(a * b) // math.gcd(a, b)
    return reduce(lcm, args)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n', 0)
            chain = witness.get('chain', [])
        else:
            n = 0
            chain = list(witness)
            
        if not isinstance(n, int) or n < 0:
            h1 = False
        else:
            if all(isinstance(c, int) for c in chain):
                h1 = True
            else:
                h1 = False
                
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            if not chain:
                k = 1
            else:
                if n == 0:
                    k = compute_lcm([abs(c) for c in chain])
                else:
                    k = compute_lcm([math.gcd(c, n) for c in chain])
            
            if n == 0:
                is_prime = (k == 0) or sympy.isprime(k)
            else:
                k_gcd = math.gcd(k, n)
                is_prime = sympy.isprime(k_gcd)
                
            neg_q = not is_prime
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The intersection of the ideals is not a prime ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1