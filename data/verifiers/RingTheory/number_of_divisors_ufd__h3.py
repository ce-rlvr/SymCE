import math
import sympy
from sympy import S

Z = S.Integers

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the conjecture.
    Witness is expected to be a tuple: (a, exponents)
    where `a` is an integer (element of UFD Z) and `exponents` is a list of integers e_i.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        a, exponents = witness
        h1 = isinstance(a, int) or a in Z
    except Exception:
        h1 = False
        
    try:
        a, exponents = witness
        h2 = (a != 0) and (abs(a) != 1)
    except Exception:
        h2 = False
        
    try:
        a, exponents = witness
        actual_divisors = sympy.divisor_count(abs(a))
        formula_divisors = math.prod(e + 1 for e in exponents)
        neg_q = (actual_divisors != formula_divisors)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a is a non-zero, non-unit element of R",
    "¬Q: The number of non-associate divisors of a in R is NOT exactly the product (e_1 + 1)(e_2 + 1) ... (e_k + 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2