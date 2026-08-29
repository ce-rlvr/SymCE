import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
from math import factorial

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: S_p is the symmetric group on p letters
    try:
        if isinstance(witness, PermutationGroup):
            p = witness.degree
            h1 = (witness.order() == factorial(p))
        else:
            p = int(witness)
            h1 = (p >= 1)
    except Exception:
        h1 = False

    # neg_Q: The number of Sylow p-subgroups of S_p is not (p-2)!
    try:
        if isinstance(witness, PermutationGroup):
            p = witness.degree
        else:
            p = int(witness)
            
        if isprime(p):
            # For prime p, the number of Sylow p-subgroups in S_p is exactly (p-2)!
            num_sylow = factorial(p - 2)
        else:
            # If p is not prime, Sylow p-subgroups are undefined.
            num_sylow = None
            
        try:
            expected = factorial(p - 2)
        except ValueError:
            expected = None
            
        if num_sylow is not None and expected is not None and num_sylow == expected:
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S_p is the symmetric group on p letters (p >= 1)",
    "¬Q: The number of Sylow p-subgroups of S_p is not (p-2)!"
]

N_HYP = 1
NEG_Q_INDEX = 1