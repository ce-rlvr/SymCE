import sympy

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        h1_ok = (p > 2) and (p == witness)
    except Exception:
        h1_ok = False

    try:
        p = int(witness)
        if p != witness:
            neg_q_ok = False
        else:
            if sympy.isprime(p):
                if p > 2:
                    neg_q_ok = False
                else:
                    neg_q_ok = True
            else:
                total = 0
                for x in range(1, p):
                    # pow(x, -1, p) raises ValueError if x and p are not coprime
                    total += pow(x, -1, p)
                neg_q_ok = (total % p != 0)
    except Exception:
        # If any inverse does not exist, the sum is undefined, so the conclusion fails.
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p > 2",
    "¬Q: sum of inverses mod p is not 0 mod p (or undefined)"
]

N_HYP = 1
NEG_Q_INDEX = 1