import itertools
from sympy.ntheory import factorint
from sympy import ZZ, QQ
import sympy.abc as abc

# Top-level setup: named object bindings
# In this domain (RingTheory), we use integers n to represent the ring Z/nZ,
# and sympy domains ZZ, QQ for standard infinite rings.

def get_nilradical(ring):
    """
    Computes the nilradical for a given ring representation.
    - For an integer n, represents Z/nZ (or Z if n=0).
    - For a tuple (n1, n2), represents the direct product Z/n1Z x Z/n2Z.
    - For sympy domains like ZZ or QQ, returns {0}.
    """
    if isinstance(ring, int):
        ring = abs(ring)
        if ring == 0:
            return {0}
        if ring == 1:
            return {0}
        rad = 1
        for p in factorint(ring):
            rad *= p
        return {x for x in range(ring) if x % rad == 0}
    elif isinstance(ring, tuple) and len(ring) == 2:
        n1, n2 = ring
        N1 = get_nilradical(n1)
        N2 = get_nilradical(n2)
        return set(itertools.product(N1, N2))
    elif ring in (ZZ, QQ):
        return {ring.zero}
    elif hasattr(ring, 'is_IntegralDomain') and ring.is_IntegralDomain:
        return {ring.zero}
    raise ValueError("Unsupported ring format")

def is_comm_ring(r):
    """
    Checks if the given object represents a commutative ring.
    """
    if isinstance(r, int):
        return True
    if r in (ZZ, QQ):
        return True
    if hasattr(r, 'is_CommutativeRing') and r.is_CommutativeRing:
        return True
    return False

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if it falsifies the conclusion.
    
    The witness should provide R, R1, and R2.
    It can be a dictionary {'R': ..., 'R1': ..., 'R2': ...} or a tuple (R, R1, R2).
    """
    try:
        if isinstance(witness, dict):
            R = witness['R']
            R1 = witness['R1']
            R2 = witness['R2']
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            R, R1, R2 = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: Let R1 and R2 be commutative rings.
    try:
        h1_ok = is_comm_ring(R1) and is_comm_ring(R2)
    except Exception:
        h1_ok = False
        
    # neg_Q: The nilradical of R is NOT equal to the direct product of the nilradicals of R1 and R2.
    try:
        N_R = get_nilradical(R)
        N_R1 = get_nilradical(R1)
        N_R2 = get_nilradical(R2)
        
        prod = set(itertools.product(N_R1, N_R2))
        
        # If R is not the direct product of R1 and R2, their nilradicals will generally not be equal.
        neg_q_ok = (N_R != prod)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R1 and R2 are commutative rings",
    "¬Q: The nilradical of R is not equal to the direct product of the nilradicals of R1 and R2"
]

N_HYP = 1
NEG_Q_INDEX = 1