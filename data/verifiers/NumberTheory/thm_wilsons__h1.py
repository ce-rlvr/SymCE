import math
import sympy

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        if p < 1:
            neg_q = False
        else:
            is_p_prime = sympy.isprime(p)
            fact_mod = math.factorial(p - 1) % p
            minus_one_mod = (-1) % p
            congruence_holds = (fact_mod == minus_one_mod)
            
            neg_q = (is_p_prime != congruence_holds)
            
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence (p is prime iff (p-1)! == -1 mod p) fails"
]

N_HYP = 0
NEG_Q_INDEX = 0