import sympy
from sympy import isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.domains import ZZ, QQ

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Interpret an integer n as the ring Z/nZ
    try:
        if isinstance(witness, (int, float)) or (hasattr(witness, 'is_integer') and witness.is_integer) or (isinstance(witness, str) and witness.isdigit()):
            n = int(witness)
            if n >= 2:
                h1 = True  # Z/nZ is finite, hence right Artinian
                neg_q = not isprime(n)  # Z/nZ is simple iff n is prime
            return [h1, neg_q]
    except Exception:
        pass

    # Interpret a string like "Z/4Z"
    try:
        if isinstance(witness, str):
            s = witness.replace(' ', '')
            if s.startswith('Z/') and s.endswith('Z'):
                n_str = s[2:-1]
                if n_str.isdigit():
                    n = int(n_str)
                    if n >= 2:
                        h1 = True
                        neg_q = not isprime(n)
                    return [h1, neg_q]
    except Exception:
        pass

    # Interpret a finite group's order as n for the ring Z/nZ
    try:
        if hasattr(witness, 'order'):
            n = int(witness.order())
            if n >= 2:
                h1 = True
                neg_q = not isprime(n)
            return [h1, neg_q]
    except Exception:
        pass

    # Interpret SymPy domains (e.g., QQ, ZZ)
    try:
        if hasattr(witness, 'is_Field'):
            if witness.is_Field:
                h1 = True  # Fields are Artinian
                neg_q = False  # Fields are simple
                return [h1, neg_q]
            elif witness == ZZ:
                h1 = False  # ZZ is not Artinian
                neg_q = True  # ZZ is not simple
                return [h1, neg_q]
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: R is not a simple ring"
]

N_HYP = 1
NEG_Q_INDEX = 1