import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import sympy.ntheory

# Top-level setup: named object bindings
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
    size = None
    try:
        if hasattr(witness, 'order') and callable(witness.order):
            size = int(witness.order())
            h1 = True
        elif hasattr(witness, '__len__'):
            size = int(len(witness))
            h1 = True
        elif hasattr(witness, 'is_FiniteSet') and witness.is_FiniteSet:
            size = int(len(witness))
            h1 = True
        elif isinstance(witness, (int, sympy.Integer)) and witness >= 0:
            size = int(witness)
            h1 = True
    except Exception:
        h1 = False

    neg_q = False
    try:
        if h1 and size is not None:
            if size <= 1:
                is_prime_power = False
            else:
                factors = sympy.ntheory.factorint(size)
                if len(factors) == 1:
                    p = list(factors.keys())[0]
                    is_prime_power = bool(sympy.ntheory.isprime(p))
                else:
                    is_prime_power = False
            neg_q = not is_prime_power
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F has a finite number of elements",
    "¬Q: The number of elements in F is not p^n for any prime p and positive integer n"
]

N_HYP = 1
NEG_Q_INDEX = 1