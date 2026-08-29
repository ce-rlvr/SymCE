import sympy
from sympy.ntheory import isprime

def conditions(witness) -> list[bool]:
    try:
        a, p = witness
        a = int(a)
        p = int(p)
    except Exception:
        return [False, False]

    # H_1: p is a prime number
    try:
        h1 = isprime(p)
    except Exception:
        h1 = False

    # ¬Q: The modular inverse of a modulo p satisfies the congruence
    # a^{-1} \equiv -\lfloor p/a \rfloor (p \bmod a)^{-1} \pmod p
    try:
        if a == 0:
            neg_q = True
        else:
            try:
                lhs = pow(a, -1, p)
            except ValueError:
                lhs = None

            try:
                rem = p % a
                inv_rem = pow(rem, -1, p)
                floor_div = p // a
                rhs = (-floor_div * inv_rem) % p
            except (ValueError, ZeroDivisionError):
                rhs = None

            if lhs is None or rhs is None:
                neg_q = True
            else:
                neg_q = (lhs % p) != (rhs % p)
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: a^{-1} is not congruent to -floor(p/a) * (p mod a)^{-1} mod p (or is undefined)"
]

N_HYP = 1
NEG_Q_INDEX = 1