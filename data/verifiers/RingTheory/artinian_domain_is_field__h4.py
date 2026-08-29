import sympy
import sympy.ntheory
from sympy import ZZ, QQ

# Named object bindings for convenience
Z4 = 4
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness can be an integer n (representing the ring Z/nZ), a tuple (ZZ, n),
    a SymPy set (like S.Integers), or a SymPy domain (like ZZ or QQ).
    """
    try:
        # Integer n represents the ring Z/nZ
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n >= 2:
                h1 = True  # Z/nZ is a commutative ring
                h2 = True  # Z/nZ has a multiplicative identity (1)
                h3 = True  # Z/nZ is finite, hence an Artinian ring
                neg_q = not sympy.ntheory.isprime(n)  # Z/nZ is a field iff n is prime
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        # Tuple (ZZ, n) represents Z/nZ
        if isinstance(witness, tuple) and len(witness) == 2:
            if witness[0] == ZZ and isinstance(witness[1], (int, sympy.Integer)):
                n = int(witness[1])
                if n >= 2:
                    h1 = True
                    h2 = True
                    h3 = True
                    neg_q = not sympy.ntheory.isprime(n)
                    return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        # SymPy sets
        if witness == sympy.S.Integers:
            return [True, True, False, True]  # ZZ is commutative, has identity, NOT Artinian, NOT a field
        if witness in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            return [True, True, True, False]  # Fields are commutative, have identity, ARE Artinian, ARE fields
    except Exception:
        pass

    try:
        # SymPy domains
        if hasattr(witness, 'is_Field'):
            h1 = True  # Standard SymPy domains (ZZ, QQ, etc.) are commutative
            h2 = True  # They have a multiplicative identity
            if witness.is_Field:
                h3 = True
                neg_q = False
            elif witness == ZZ:
                h3 = False
                neg_q = True
            else:
                h3 = False
                neg_q = not witness.is_Field
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "H_3: R is an Artinian ring",
    "¬Q: R is not a field"
]

N_HYP = 3
NEG_Q_INDEX = 3