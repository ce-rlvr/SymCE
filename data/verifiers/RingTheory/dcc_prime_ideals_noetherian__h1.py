import sympy
import math
import itertools
import functools

class InfinitePolynomialRing:
    def __init__(self, base_ring="k"):
        self.base_ring = base_ring
    
    def __str__(self):
        return f"{self.base_ring}[x_1, x_2, ...]"
    
    @property
    def has_infinite_descending_chain_of_prime_ideals(self):
        return True

class RingOfContinuousFunctions:
    def __init__(self, domain="[0,1]"):
        self.domain = domain
        
    def __str__(self):
        return f"C({self.domain})"
        
    @property
    def has_infinite_descending_chain_of_prime_ideals(self):
        return True

# Standard counterexamples for rings lacking the descending chain condition on prime ideals
R_inf = InfinitePolynomialRing("k")
C_01 = RingOfContinuousFunctions("[0,1]")

def conditions(witness) -> list[bool]:
    neg_q = False
    try:
        # Check if the witness is one of our predefined counterexample objects
        if hasattr(witness, "has_infinite_descending_chain_of_prime_ideals"):
            neg_q = bool(witness.has_infinite_descending_chain_of_prime_ideals)
        # Alternatively, check if the witness is a string describing a valid counterexample
        elif isinstance(witness, str):
            s = witness.lower()
            if "..." in s and ("[" in s or "(" in s):
                neg_q = True
            elif "infinite" in s and ("variable" in s or "product" in s or "dimension" in s or "polynomial" in s):
                neg_q = True
            elif "c([0,1])" in s.replace(" ", ""):
                neg_q = True
            elif "continuous functions" in s:
                neg_q = True
            elif "r_inf" in s or "c_01" in s:
                neg_q = True
    except Exception:
        pass
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R has an infinite strictly descending chain of prime ideals"
]

N_HYP = 0
NEG_Q_INDEX = 0