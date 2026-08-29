import math
import sympy

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        p = sympy.Rational(witness)
        if p.denominator != 1:
            return [False]
        p = int(p)
        if p < 2:
            return [False]
        
        if p <= 100000:
            fact = math.factorial(p - 2)
            neg_q = bool((fact % p) != 1)
        else:
            fact_mod = 1
            for i in range(1, p - 1):
                fact_mod = (fact_mod * i) % p
            neg_q = bool(fact_mod != 1)
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = ["¬Q: ((p-2)!)^{-1} is not 1 mod p"]
N_HYP = 0
NEG_Q_INDEX = 0