import sympy
from sympy.ntheory import isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that p is a prime.
    """
    try:
        # Extract n and p from the witness
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
        elif hasattr(witness, 'n') and hasattr(witness, 'p'):
            n = witness.n
            p = witness.p
        elif isinstance(witness, (tuple, list)) and len(witness) >= 2:
            n, p = witness[0], witness[1]
        else:
            return [False, False, False, False]
            
        # H_1: n is a positive integer
        try:
            h1 = bool(int(n) == n and n > 0)
        except Exception:
            h1 = False
            
        # H_2: G is the general linear group GL_n(F_p)
        # For F_p (or Z/pZ) to be a valid ring, p must be an integer >= 2
        try:
            h2 = bool(int(p) == p and p >= 2)
        except Exception:
            h2 = False
            
        # H_3: U is the subgroup of G consisting of all upper unitriangular matrices
        # This is a definitional hypothesis, always true for valid n and p
        h3 = True
        
        # ¬Q: U is NOT a Sylow p-subgroup of G
        # Sylow p-subgroups are only defined for primes. If p is not prime, 
        # the conclusion that U is a Sylow p-subgroup is false.
        try:
            neg_q = not isprime(int(p))
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is the general linear group GL_n(F_p)",
    "H_3: U is the subgroup of G consisting of all upper unitriangular matrices",
    "¬Q: U is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3