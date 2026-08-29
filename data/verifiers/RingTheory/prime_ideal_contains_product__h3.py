import sympy
from sympy import Rational, isprime

ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def check_subset(A, P):
    if hasattr(A, 'is_subset'):
        try:
            return bool(A.is_subset(P))
        except Exception:
            pass
    if hasattr(P, 'contains'):
        try:
            res = P.contains(A)
            if res is not NotImplemented:
                return bool(res)
        except Exception:
            pass
            
    if isinstance(A, (list, set, tuple)):
        if not A:
            return True
        return all(check_subset(a, P) for a in A)
        
    try:
        if isinstance(A, int):
            val_A = A
        elif hasattr(A, 'is_integer') and A.is_integer:
            val_A = int(A)
        elif isinstance(A, float) and A.is_integer():
            val_A = int(A)
        else:
            return False
    except Exception:
        return False
        
    try:
        if isinstance(P, int):
            val_P = P
        elif hasattr(P, 'is_integer') and P.is_integer:
            val_P = int(P)
        elif isinstance(P, float) and P.is_integer():
            val_P = int(P)
        else:
            return False
    except Exception:
        return False
        
    if val_P == 0:
        return val_A == 0
    return val_A % val_P == 0

def conditions(witness) -> list[bool]:
    if hasattr(witness, 'is_commutative_ring') and callable(witness.is_commutative_ring):
        try:
            h1 = witness.is_commutative_ring()
            h2 = witness.is_prime_ideal_P() if hasattr(witness, 'is_prime_ideal_P') else witness.is_prime_ideal()
            h3 = witness.is_ideal_J()
            h4 = witness.IJ_subset_P()
            neg_q = not witness.conclusion()
            return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
        except Exception:
            pass

    try:
        if isinstance(witness, dict):
            P = witness['P']
            J = witness['J']
            I = witness['I']
        elif hasattr(witness, 'P') and hasattr(witness, 'J') and hasattr(witness, 'I'):
            P = witness.P
            J = witness.J
            I = witness.I
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                P, J, I = witness[0], witness[1], witness[2]
            elif len(witness) >= 4:
                if hasattr(witness[0], 'is_commutative') or witness[0] in (ZZ, QQ):
                    P, J, I = witness[1], witness[2], witness[3]
                else:
                    P, J, I = witness[0], witness[1], witness[2]
            else:
                return [False] * 5
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    h1 = True

    try:
        if hasattr(P, 'is_prime'):
            if callable(P.is_prime):
                h2 = bool(P.is_prime())
            else:
                h2 = bool(P.is_prime)
        else:
            if isinstance(P, int):
                h2 = isprime(abs(P))
            elif hasattr(P, 'is_integer') and P.is_integer:
                h2 = isprime(abs(int(P)))
            elif isinstance(P, float) and P.is_integer():
                h2 = isprime(abs(int(P)))
            else:
                h2 = False
    except Exception:
        h2 = False

    try:
        if hasattr(J, 'is_ideal'):
            if callable(J.is_ideal):
                h3 = bool(J.is_ideal())
            else:
                h3 = bool(J.is_ideal)
        else:
            if isinstance(J, int):
                h3 = True
            elif hasattr(J, 'is_integer') and J.is_integer:
                h3 = True
            elif isinstance(J, float) and J.is_integer():
                h3 = True
            else:
                h3 = False
    except Exception:
        h3 = False

    try:
        if hasattr(witness, 'IJ_subset_P') and callable(witness.IJ_subset_P):
            h4 = bool(witness.IJ_subset_P())
        else:
            if isinstance(I, (list, set, tuple)):
                IJ = [i * J for i in I]
            else:
                IJ = I * J
            h4 = bool(check_subset(IJ, P))
    except Exception:
        h4 = False

    try:
        if hasattr(witness, 'conclusion') and callable(witness.conclusion):
            neg_q = not bool(witness.conclusion())
        else:
            I_subset = check_subset(I, P)
            J_subset = check_subset(J, P)
            neg_q = not (I_subset or J_subset)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal of R",
    "H_3: J is an ideal of R",
    "H_4: The product ideal IJ is a subset of P",
    "¬Q: Neither I nor J is a subset of P"
]

N_HYP = 4
NEG_Q_INDEX = 4