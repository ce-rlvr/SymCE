import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def count_sq_roots_of_1(n):
    """
    Counts the number of solutions to x^2 = 1 mod n.
    This corresponds to the number of elements in the center of SL(2, Z/nZ).
    """
    if n == 0:
        return 2
    if n == 1:
        return 1
    n = abs(n)
    factors = factorint(n)
    count = 1
    for p, e in factors.items():
        if p == 2:
            if e == 1:
                count *= 1
            elif e == 2:
                count *= 2
            else:
                count *= 4
        else:
            count *= 2
    return count

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to be an integer n (representing the ring Z/nZ),
    or a sympy domain/ring.
    """
    try:
        if isinstance(witness, tuple) or isinstance(witness, list):
            F = witness[0]
        else:
            F = witness
            
        if hasattr(F, 'characteristic') and callable(F.characteristic):
            char = F.characteristic()
            if hasattr(F, 'is_Field') and F.is_Field:
                sols = 2 if char != 2 else 1
            else:
                n = int(char)
                sols = count_sq_roots_of_1(n)
        else:
            if F == sympy.ZZ:
                char = 0
                n = 0
            else:
                n = int(F)
                char = n
            sols = count_sq_roots_of_1(n)
            
        h1_ok = (char != 2)
        h2_ok = True  # G is SL(2, F) by the structural definition of the witness
        neg_q_ok = (sols != 2)
        
        return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: The characteristic of F is not equal to 2",
    "H_2: G is the special linear group SL(2, F)",
    "¬Q: The center Z(G) does not consist of exactly two elements"
]

N_HYP = 2
NEG_Q_INDEX = 2