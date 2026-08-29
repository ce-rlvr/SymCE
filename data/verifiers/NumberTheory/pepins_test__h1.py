import sympy

def conditions(witness):
    try:
        if int(witness) == witness and witness >= 0:
            n = int(witness)
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            F_n = 2**(2**n) + 1
            is_prime = sympy.isprime(F_n)
            power = (F_n - 1) // 2
            val = pow(3, power, F_n)
            cong = (val == F_n - 1)
            neg_q = bool(is_prime != cong)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F_n is the n-th Fermat number defined by F_n = 2^{2^n} + 1",
    "¬Q: F_n is prime is NOT equivalent to 3^{(F_n - 1)/2} == -1 (mod F_n)"
]

N_HYP = 1
NEG_Q_INDEX = 1