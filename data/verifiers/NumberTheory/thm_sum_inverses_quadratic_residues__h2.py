import sympy
import math
import itertools
import functools

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(witness))
    except Exception:
        h1 = False

    # ¬Q: \sum_{r \in QR(p)} r^{-1} \not\equiv 0 \pmod p
    try:
        p = int(witness)
        if p <= 1:
            neg_q = False
        else:
            qrs = set()
            for x in range(1, p):
                qrs.add((x * x) % p)
            
            if 0 in qrs:
                qrs.remove(0)
                
            sum_inv = 0
            for r in qrs:
                sum_inv += pow(r, -1, p)
            
            neg_q = bool((sum_inv % p) != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: sum of inverses of quadratic residues is not 0 mod p"
]

N_HYP = 1
NEG_Q_INDEX = 1