import sympy
from sympy import ZZ, QQ

# Top-level setup for potential witness expressions
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    if isinstance(witness, bool):
        return [False, False]

    # Normalize string representations
    try:
        if isinstance(witness, str):
            w_upper = witness.upper()
            if w_upper == "ZZ":
                witness = ZZ
            elif w_upper == "QQ":
                witness = QQ
            elif w_upper.startswith("Z"):
                try:
                    witness = int(w_upper[1:])
                except ValueError:
                    pass
    except Exception:
        pass

    h1 = False
    try:
        # We interpret an integer n as the ring Z/nZ (with n=0 being Z).
        if isinstance(witness, (int, sympy.Integer)):
            n = abs(int(witness))
            # Z/1Z is the zero ring, which is not a non-zero ring.
            if n != 1:
                h1 = True
        elif witness in (ZZ, QQ):
            h1 = True
    except Exception:
        pass

    neg_q = False
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = abs(int(witness))
            if n == 0:
                # Z has infinitely many prime ideals
                neg_q = True
            elif n > 1:
                # The prime ideals of Z/nZ correspond to the prime factors of n.
                # It has exactly one prime ideal iff n has exactly one distinct prime factor.
                num_primes = len(sympy.primefactors(n))
                neg_q = (num_primes != 1)
        elif witness == ZZ:
            # ZZ has infinitely many prime ideals
            neg_q = True
        elif witness == QQ:
            # QQ is a field, it has exactly one prime ideal: (0)
            neg_q = False
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a non-zero commutative ring with identity",
    "¬Q: R does not have exactly one prime ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1