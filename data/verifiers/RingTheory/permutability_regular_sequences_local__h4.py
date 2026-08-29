import math
import itertools
import sympy
from sympy import factorint, eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to represent a finite local ring Z/nZ and a sequence of integers.
    It can be provided as a tuple (n, sequence) or just the sequence (defaulting to n=4).
    """
    try:
        if isinstance(witness, dict):
            ring_n = witness.get('n', 4)
            seq = witness.get('seq', [])
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                try:
                    # Try to unpack as (n, seq)
                    ring_n = abs(int(witness[0]))
                    seq = [int(val) for val in witness[1]]
                except (TypeError, ValueError):
                    # Fallback: treat the whole witness as the sequence
                    ring_n = 4
                    seq = [int(val) for val in witness]
            else:
                # Fallback: treat the whole witness as the sequence
                ring_n = 4
                seq = [int(val) for val in witness]
        else:
            return [False, False, False, False]
            
        ring_n = abs(int(ring_n))
        seq = [int(val) for val in seq]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative Noetherian ring
    # Z/nZ is finite, hence always commutative and Noetherian for n >= 2.
    try:
        h1 = (ring_n >= 2)
    except Exception:
        h1 = False

    # H_2: R is a local ring with maximal ideal m
    # Z/nZ is a local ring if and only if n is a prime power p^k (k >= 1).
    try:
        factors = factorint(ring_n)
        factors = {p: k for p, k in factors.items() if p != -1}
        h2 = (len(factors) == 1)
    except Exception:
        h2 = False

    def is_regular_sequence(sequence):
        g = ring_n
        for val in sequence:
            # In Z/gZ, an element 'val' is a zero-divisor iff gcd(val, g) > 1.
            # If g == 1, Z/gZ is the zero ring, where no element is a zero-divisor.
            if g != 1 and math.gcd(val, g) != 1:
                return False
            g = math.gcd(g, val)
        return True

    # H_3: The sequence x_1, x_2, ..., x_n is a regular sequence in R
    try:
        h3 = is_regular_sequence(seq)
    except Exception:
        h3 = False

    # ¬Q: There exists a permutation of the sequence that is NOT a regular sequence in R
    try:
        neg_q = False
        for p in itertools.permutations(seq):
            if not is_regular_sequence(p):
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: R is a local ring with maximal ideal m",
    "H_3: The sequence x_1, x_2, ..., x_n is a regular sequence in R",
    "¬Q: There exists a permutation of the sequence that is not a regular sequence in R"
]

N_HYP = 3
NEG_Q_INDEX = 3