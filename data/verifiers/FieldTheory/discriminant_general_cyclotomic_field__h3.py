import sympy
from sympy import Poly, Expr, exp, pi, I, sympify, simplify, N, discriminant, Integer
from sympy.ntheory import primefactors, totient
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def get_discriminant(K):
    if isinstance(K, str):
        try:
            K = sympify(K)
        except Exception:
            pass
    if isinstance(K, Poly):
        return K.discriminant()
    try:
        free = K.free_symbols
        if len(free) == 1:
            gen = list(free)[0]
            return discriminant(K, gen)
    except Exception:
        pass
    try:
        if isinstance(K, (list, tuple)):
            return Poly(K, x).discriminant()
    except Exception:
        pass
    try:
        return K.discriminant()
    except Exception:
        pass
    return None

def formula(n):
    phi_n = totient(n)
    sign = (-1)**(phi_n // 2)
    num = n**phi_n
    den = 1
    for p in primefactors(n):
        den *= p**(phi_n // (p - 1))
    return sign * num // den

def conditions(witness) -> list[bool]:
    n = None
    zeta_n = None
    K = None

    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            zeta_n = witness.get('zeta_n')
            K = witness.get('K')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                n, zeta_n, K = witness
            elif len(witness) == 2:
                n = witness[0]
                if isinstance(witness[1], Poly) or (isinstance(witness[1], Expr) and witness[1].free_symbols) or isinstance(witness[1], (list, tuple, str)):
                    K = witness[1]
                    zeta_n = exp(2*I*pi/n)
                else:
                    zeta_n = witness[1]
                    K = None
        else:
            n = witness
            zeta_n = exp(2*I*pi/n)
            K = None
    except Exception:
        pass

    # H1: n is an integer strictly greater than 2
    try:
        h1 = isinstance(n, (int, Integer)) and n > 2
    except Exception:
        h1 = False

    # H2: zeta_n is a primitive n-th root of unity
    try:
        if h1 and zeta_n is not None:
            z = sympify(zeta_n)
            val_n = simplify(z**n)
            
            is_root = False
            if val_n == 1:
                is_root = True
            else:
                try:
                    if abs(complex(N(val_n)) - 1.0) <= 1e-9:
                        is_root = True
                except Exception:
                    pass
            
            if is_root:
                h2 = True
                for p in primefactors(n):
                    val_p = simplify(z**(n//p))
                    if val_p == 1:
                        h2 = False
                        break
                    try:
                        if abs(complex(N(val_p)) - 1.0) <= 1e-9:
                            h2 = False
                            break
                    except Exception:
                        pass
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: Discriminant of K over Q is NOT equal to the formula
    try:
        if h1 and K is not None:
            disc_K = get_discriminant(K)
            if disc_K is not None:
                expected = formula(n)
                neg_q = (disc_K != expected)
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 2",
    "H_2: zeta_n is a primitive n-th root of unity",
    "¬Q: The discriminant of K over Q is not equal to the formula"
]

N_HYP = 2
NEG_Q_INDEX = 2