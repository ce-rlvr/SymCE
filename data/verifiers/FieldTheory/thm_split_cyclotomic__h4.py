import sympy
import sympy.abc
from sympy import GF, QQ, RR, CC, S
import math

def check_q_holds(n, F, K):
    n = int(n)
    
    # Finite fields
    if hasattr(K, 'is_FiniteField') and K.is_FiniteField:
        if not (hasattr(F, 'is_FiniteField') and F.is_FiniteField):
            return False
        if F.characteristic() != K.characteristic():
            return False
        if K.degree % F.degree != 0:
            return False
        if (K.order - 1) % n != 0:
            return False
        
        q = int(F.order)
        if n == 1:
            d = 1
        else:
            if math.gcd(q, n) != 1:
                return False
            d = 1
            val = q % n
            while val != 1:
                val = (val * q) % n
                d += 1
        return K.order == q ** d

    # Rational field
    if F == QQ and K == QQ:
        if n in (1, 2):
            return True
        return False
        
    # Real and Complex fields
    if F in (RR, S.Reals) and K in (RR, S.Reals):
        if n in (1, 2):
            return True
        return False
        
    if F in (CC, S.Complexes) and K in (CC, S.Complexes):
        return True
        
    if F in (RR, S.Reals) and K in (CC, S.Complexes):
        if n > 2:
            return True
        return False

    raise NotImplementedError("Field type not supported for Q check")

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            F = witness.get('F')
            K = witness.get('K')
        else:
            n, F, K = witness
    except Exception:
        return [False, False, False, False]

    # H1: n is a positive integer
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    # H2: F is a field
    try:
        if F in (S.Reals, S.Complexes):
            h2 = True
        else:
            h2 = hasattr(F, 'is_Field') and F.is_Field
    except Exception:
        h2 = False

    # H3: The characteristic of F does not divide n
    try:
        if F in (S.Reals, S.Complexes):
            char = 0
        else:
            char = F.characteristic()
            
        if char == 0:
            h3 = True
        else:
            h3 = (n % char != 0)
    except Exception:
        h3 = False

    # neg_Q: K != F(\zeta) for any primitive n-th root of unity \zeta in K
    try:
        q_holds = check_q_holds(n, F, K)
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: F is a field",
    "H_3: The characteristic of F does not divide n",
    "¬Q: K is not F(\\zeta) for any primitive n-th root of unity \\zeta in K"
]

N_HYP = 3
NEG_Q_INDEX = 3