import sympy
import math
import functools

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ
Z = ZZ
Q = QQ
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, P = witness
        else:
            R = ZZ
            P = witness

        # If P is already a sympy ideal with these methods
        if hasattr(P, 'is_prime') and hasattr(P, 'is_maximal'):
            try:
                return [bool(P.is_prime()), not bool(P.is_maximal())]
            except Exception:
                pass

        # Check for the ring of integers
        if R == ZZ:
            if isinstance(P, (int, sympy.Integer)):
                n = abs(int(P))
            elif isinstance(P, (list, tuple, set)):
                if not P:
                    n = 0
                else:
                    n = abs(functools.reduce(math.gcd, [int(i) for i in P]))
            else:
                return [False, False]
                
            is_prime = (n == 0 or sympy.isprime(n))
            is_maximal = sympy.isprime(n)
            
            return [is_prime, not is_maximal]

        # If R can create ideals
        if hasattr(R, 'ideal'):
            try:
                if isinstance(P, (list, tuple, set)):
                    ideal = R.ideal(*P)
                else:
                    ideal = R.ideal(P)
                if hasattr(ideal, 'is_prime') and hasattr(ideal, 'is_maximal'):
                    return [bool(ideal.is_prime()), not bool(ideal.is_maximal())]
            except Exception:
                pass

        # Fallback for P = 0 in other rings
        if P == 0 or P == [0] or P == (0,):
            if hasattr(R, 'is_IntegralDomain') and hasattr(R, 'is_Field'):
                is_prime = bool(R.is_IntegralDomain)
                is_maximal = bool(R.is_Field)
                return [is_prime, not is_maximal]
                
    except Exception:
        pass
        
    return [False, False]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "¬Q: P is not a maximal ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1