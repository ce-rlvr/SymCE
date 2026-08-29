import math
import functools
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (sigma, [c_1, ..., c_k]) or just a list of cycles [c_1, ..., c_k].
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            sigma, cycles = witness
        elif isinstance(witness, list):
            cycles = witness
            if not cycles:
                return [False, False, False, False]
            sigma = cycles[0]
            for c in cycles[1:]:
                sigma = sigma * c
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: sigma is a permutation
    try:
        h1 = isinstance(sigma, Permutation)
    except Exception:
        h1 = False

    # H_2: c_i are cycles
    try:
        h2 = isinstance(cycles, (list, tuple)) and len(cycles) > 0
        if h2:
            for c in cycles:
                if not isinstance(c, Permutation):
                    h2 = False
                    break
                # A cycle has at most one orbit of length > 1
                non_trivial = [cyc for cyc in c.cyclic_form if len(cyc) > 1]
                if len(non_trivial) > 1:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H_3: sigma is the product of c_1, ..., c_k
    try:
        if h1 and h2:
            prod = cycles[0]
            for c in cycles[1:]:
                prod = prod * c
            h3 = bool(sigma == prod)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The order of sigma is NOT the least common multiple of the cycle lengths
    try:
        if h1 and h2:
            m = []
            for c in cycles:
                non_trivial = [cyc for cyc in c.cyclic_form if len(cyc) > 1]
                if non_trivial:
                    m.append(len(non_trivial[0]))
                else:
                    m.append(1)
            
            lcm = 1
            for length in m:
                lcm = (lcm * length) // math.gcd(lcm, length)
            
            neg_q = bool(sigma.order() != lcm)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: sigma is a permutation",
    "H_2: c_i are cycles",
    "H_3: sigma is the product of c_1, ..., c_k",
    "¬Q: The order of sigma is not the least common multiple of the cycle lengths"
]

N_HYP = 3
NEG_Q_INDEX = 3