import sympy
import sympy.polys
import sympy.abc
import math
import itertools
import functools

ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            w = witness[-1]
        else:
            w = witness
            
        if hasattr(w, 'gen'):
            w = w.gen
        elif hasattr(w, 'gens') and len(w.gens) == 1:
            w = list(w.gens)[0]
            
        if isinstance(w, int):
            n = w
        else:
            s = str(w).replace('Z', '').replace('*', '').replace('<', '').replace('>', '').replace(' ', '')
            if s == '':
                n = 1
            elif s == '-':
                n = -1
            else:
                n = int(s)
                
        # H_1: R is a commutative ring
        # We evaluate this in the context of R = Z, which is a commutative ring.
        h1_ok = True
        
        # Q: The extended ideal is a prime ideal in the polynomial ring
        # For R = Z and P = nZ, P[x] is prime iff n is prime or n == 0.
        is_prime_ideal = sympy.isprime(abs(n)) or n == 0
        neg_q_ok = not is_prime_ideal
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The extended ideal is not prime in the polynomial ring"
]

N_HYP = 1
NEG_Q_INDEX = 1