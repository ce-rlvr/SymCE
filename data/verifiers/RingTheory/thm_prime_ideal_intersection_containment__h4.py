import sympy
from sympy import isprime
from sympy.abc import x, y, z

Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                P, I, J = witness
            elif len(witness) == 4:
                R, P, I, J = witness
            else:
                return [False, False, False, False]
        elif isinstance(witness, dict):
            P = witness.get('P')
            I = witness.get('I')
            J = witness.get('J')
            if P is None or I is None or J is None:
                return [False, False, False, False]
        else:
            return [False, False, False, False]

        def unwrap(obj):
            if isinstance(obj, (list, tuple, set)) and len(obj) == 1:
                return list(obj)[0]
            return obj

        P = unwrap(P)
        I = unwrap(I)
        J = unwrap(J)

        # Try to interpret as integers (generators of ideals in Z)
        try:
            if isinstance(P, float) or isinstance(I, float) or isinstance(J, float):
                raise ValueError
            
            p = int(P)
            i = int(I)
            j = int(J)
            
            h1 = True
            h2 = (p == 0) or isprime(abs(p))
            h3 = True
            
            if p == 0:
                i_in_p = (i == 0)
                j_in_p = (j == 0)
            else:
                i_in_p = (i % p == 0)
                j_in_p = (j % p == 0)
                
            neg_q = not (i_in_p or j_in_p)
            return [h1, h2, h3, neg_q]
        except (ValueError, TypeError):
            pass
            
        # If not integers, maybe they are SymPy ideals
        try:
            h1 = True
            h2 = bool(P.is_prime)
            h3 = True
            i_in_p = bool(I.subset(P))
            j_in_p = bool(J.subset(P))
            neg_q = not (i_in_p or j_in_p)
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal of R",
    "H_3: I and J are ideals of R",
    "¬Q: I is not contained in P and J is not contained in P"
]

N_HYP = 3
NEG_Q_INDEX = 3