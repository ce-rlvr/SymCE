import sympy
import sympy.ntheory
import math

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            S, p = int(witness[0]), int(witness[1])
        elif isinstance(witness, (int, sympy.Integer)):
            p = int(witness)
            if 1 < p <= 100000:
                phi = sympy.ntheory.totient(p)
                factors = sympy.ntheory.factorint(phi).keys()
                roots = []
                for g in range(1, p):
                    if math.gcd(g, p) == 1:
                        is_root = True
                        for q in factors:
                            if pow(g, phi // q, p) == 1:
                                is_root = False
                                break
                        if is_root:
                            roots.append(g)
                S = sum(roots)
            else:
                S = 0
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    if p > 100000:
        return [False, False]
        
    try:
        if p <= 1:
            h1 = False
        else:
            phi = sympy.ntheory.totient(p)
            factors = sympy.ntheory.factorint(phi).keys()
            roots = []
            for g in range(1, p):
                if math.gcd(g, p) == 1:
                    is_root = True
                    for q in factors:
                        if pow(g, phi // q, p) == 1:
                            is_root = False
                            break
                    if is_root:
                        roots.append(g)
            
            expected_sum = sum(roots)
            h1 = (S % p == expected_sum % p)
    except Exception:
        h1 = False

    try:
        if p <= 1:
            neg_q = False
        else:
            mu = sympy.ntheory.mobius(p - 1)
            neg_q = (S % p) != (mu % p)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S is the sum of a complete set of incongruent primitive roots modulo p",
    "¬Q: S is not congruent to mu(p-1) modulo p"
]

N_HYP = 1
NEG_Q_INDEX = 1