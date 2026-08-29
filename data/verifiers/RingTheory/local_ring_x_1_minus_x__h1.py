import math
import sympy
from sympy.ntheory import primefactors
from sympy import Rational
from sympy.abc import x, y, z

# Top-level setup
# Integers are used directly to represent the rings Z/nZ.
# For example, witness = 1 represents the trivial ring Z/1Z.

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    "If R has a multiplicative identity and for every x in R, either x or 1-x is a unit,
    then R is a local ring."
    """
    try:
        if type(witness) is int:
            n = witness
            if n < 1:
                return [False, False, False]
            
            # H_1: R has a multiplicative identity
            # Z/nZ always has a multiplicative identity (1 mod n)
            h1_ok = True
            
            # H_2: For every element x in R, either x or 1-x is a unit in R
            h2_ok = True
            for i in range(n):
                # In Z/nZ, an element is a unit iff it is coprime to n
                unit_x = (math.gcd(i, n) == 1)
                unit_1_x = (math.gcd((1 - i) % n, n) == 1)
                if not (unit_x or unit_1_x):
                    h2_ok = False
                    break
            
            # Conclusion: R is a local ring
            # A finite commutative ring Z/nZ is local iff it has exactly one maximal ideal.
            # Maximal ideals of Z/nZ correspond to prime factors of n.
            # Thus, Z/nZ is local iff n has exactly one prime factor (i.e., n = p^k).
            # Note: n=1 has 0 prime factors, so it is NOT local.
            is_local = (len(primefactors(n)) == 1)
            neg_q_ok = not is_local
            
            return [h1_ok, h2_ok, neg_q_ok]
            
        elif hasattr(witness, 'is_commutative'):
            # Fallback for sympy domains
            if witness.is_Field:
                return [True, True, False]
            elif witness == sympy.S.Integers:
                return [True, False, True]
                
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: For every element x in R, either x or 1-x is a unit in R",
    "¬Q: R is not a local ring"
]

N_HYP = 2
NEG_Q_INDEX = 2