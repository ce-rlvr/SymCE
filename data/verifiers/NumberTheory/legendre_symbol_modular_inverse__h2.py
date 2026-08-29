import sympy
import sympy.ntheory

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            p = witness['p']
        else:
            a, p = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(a % p != 0)
    except Exception:
        h2 = False
        
    try:
        inv_a = sympy.ntheory.mod_inverse(a, p)
        ls_inv = sympy.ntheory.legendre_symbol(inv_a, p)
        ls_a = sympy.ntheory.legendre_symbol(a, p)
        neg_q = bool(ls_inv != ls_a)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: a is not divisible by p",
    "¬Q: The Legendre symbol (a^{-1}/p) is not equal to (a/p)"
]

N_HYP = 2
NEG_Q_INDEX = 2