import sympy
import sympy.abc
from sympy import Rational, Integer
import math
import itertools
import functools

# Top-level setup for Ring Theory
x, y, z = sympy.abc.x, sympy.abc.y, sympy.abc.z
QQ = sympy.Rational
ZZ = sympy.Integer

def conditions(witness) -> list[bool]:
    neg_q = False
    
    # 1. Check if witness is an object with zero_divisors and associated_primes methods/properties
    try:
        zd = None
        ap = None
        if hasattr(witness, 'zero_divisors'):
            zd = witness.zero_divisors() if callable(witness.zero_divisors) else witness.zero_divisors
        if hasattr(witness, 'associated_primes'):
            ap = witness.associated_primes() if callable(witness.associated_primes) else witness.associated_primes
            
        if zd is not None and ap is not None:
            zd_set = set(zd)
            union_ap = set()
            for p in ap:
                union_ap.update(p)
            neg_q = zd_set != union_ap
            return [neg_q]
    except Exception:
        pass

    # 2. Check if witness is a dictionary
    try:
        if isinstance(witness, dict) and 'zero_divisors' in witness and 'associated_primes' in witness:
            zd = set(witness['zero_divisors'])
            ap = witness['associated_primes']
            union_ap = set()
            for p in ap:
                union_ap.update(p)
            neg_q = zd != union_ap
            return [neg_q]
    except Exception:
        pass

    # 3. Check if witness is a tuple (zero_divisors, associated_primes)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            zd, ap = witness
            if isinstance(zd, (set, list, tuple)) and isinstance(ap, (set, list, tuple)):
                if all(isinstance(p, (set, list, tuple)) for p in ap):
                    union_ap = set()
                    for p in ap:
                        union_ap.update(p)
                    neg_q = set(zd) != union_ap
                    return [neg_q]
    except Exception:
        pass

    # 4. Check string representation for known counterexamples
    # The theorem holds for Noetherian rings. Counterexamples must be non-Noetherian.
    # Common counterexamples: 
    # - Infinite polynomial ring modulo squares: k[x_1, x_2, ...] / (x_1^2, x_2^2, ...)
    # - Ring of continuous functions: C([0, 1])
    try:
        s = str(witness).lower().replace(" ", "")
        is_infinite_poly = ("[" in s and "/" in s and ("^2" in s or "**2" in s) and 
                            ("..." in s or "…" in s or "infinite" in s))
        is_continuous = "c([0,1])" in s or "continuous" in s
        
        if is_infinite_poly or is_continuous:
            neg_q = True
    except Exception:
        pass

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The set of zero divisors of R is not exactly the union of all associated prime ideals of R"
]
N_HYP = 0
NEG_Q_INDEX = 0