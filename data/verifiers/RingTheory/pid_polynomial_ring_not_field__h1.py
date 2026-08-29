import sympy
from sympy.abc import x

def conditions(witness) -> list[bool]:
    if witness == sympy.S.Integers:
        witness = sympy.ZZ
    elif witness == sympy.S.Rationals:
        witness = sympy.QQ
    elif witness == sympy.S.Reals:
        witness = sympy.RR
    elif witness == sympy.S.Complexes:
        witness = sympy.CC
    elif isinstance(witness, str):
        mapping = {'ZZ': sympy.ZZ, 'QQ': sympy.QQ, 'RR': sympy.RR, 'CC': sympy.CC}
        witness = mapping.get(witness, witness)

    if isinstance(witness, int):
        try:
            if witness <= 1:
                return [True, False]
            is_prime = sympy.isprime(witness)
            h1 = not is_prime
            neg_q = is_prime
            return [h1, neg_q]
        except Exception:
            pass

    try:
        h1 = not bool(witness.is_Field)
    except Exception:
        h1 = False

    try:
        neg_q = bool(witness.poly_ring(x).is_PID)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is not a field",
    "¬Q: The polynomial ring over R is a principal ideal domain"
]

N_HYP = 1
NEG_Q_INDEX = 1