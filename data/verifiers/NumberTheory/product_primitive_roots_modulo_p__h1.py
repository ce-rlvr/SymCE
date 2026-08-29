import math
from sympy.ntheory import totient, n_order

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p, R = witness
            p = int(p)
            R = set(int(r) for r in R)
        else:
            p = int(witness)
            if 2 <= p < 100000:
                phi_p = totient(p)
                R = set()
                for g in range(1, p):
                    if math.gcd(g, p) == 1:
                        try:
                            if n_order(g, p) == phi_p:
                                R.add(g)
                        except Exception:
                            pass
            else:
                R = set()
    except Exception:
        return [False, False]

    # H_1: R is the set of all primitive roots modulo p
    h1_ok = False
    try:
        if isinstance(p, int) and 2 <= p < 100000:
            phi_p = totient(p)
            expected_R = set()
            for g in range(1, p):
                if math.gcd(g, p) == 1:
                    try:
                        if n_order(g, p) == phi_p:
                            expected_R.add(g)
                    except Exception:
                        pass
            if set(R) == expected_R:
                h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: product of r in R is not congruent to (-1)^phi(p-1) mod p
    neg_q_ok = False
    try:
        if h1_ok:
            prod = 1
            for r in R:
                prod = (prod * r) % p
            
            if p - 1 >= 1:
                exponent = totient(p - 1)
                rhs = ((-1) ** exponent) % p
                if prod % p != rhs % p:
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is the set of all primitive roots modulo p",
    "not Q: product of r in R is not congruent to (-1)^phi(p-1) mod p"
]

N_HYP = 1
NEG_Q_INDEX = 1