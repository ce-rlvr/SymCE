import sympy
from sympy import sqrt, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard algebra objects
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

def get_k(witness):
    """
    Extracts the integer k such that the witness represents the ring Z[k*sqrt(2)].
    """
    if isinstance(witness, int):
        return witness
    if isinstance(witness, str):
        import re
        m = re.search(r'(\d+)\*sqrt\(2\)', witness)
        if m:
            return int(m.group(1))
        if 'sqrt(2)' in witness:
            return 1
        if witness in ("Z", "ZZ"):
            return 0
        if witness.isdigit():
            return int(witness)
    if isinstance(witness, (list, tuple, set)):
        for item in witness:
            try:
                if item == 1: 
                    continue
                val = item / sqrt(2)
                if val.is_Integer:
                    return int(val)
            except Exception:
                pass
    try:
        val = witness / sqrt(2)
        if val.is_Integer:
            return int(val)
    except Exception:
        pass
    return None

def conditions(witness) -> list[bool]:
    k = get_k(witness)
    
    # H_1: N maps R \ {0} to N.
    # This holds if and only if R is a subring of Z[sqrt(2)], which means
    # R = Z[k*sqrt(2)] for some integer k.
    try:
        h1_ok = (k is not None and isinstance(k, int))
    except Exception:
        h1_ok = False
        
    # ¬Q: R is NOT a Euclidean domain with Euclidean function N.
    # Z[k*sqrt(2)] is Euclidean with respect to N iff k = 1, -1, or 0.
    # For |k| > 1, the division algorithm fails (e.g., dividing k*sqrt(2) by k).
    try:
        if k is not None:
            neg_q = (abs(k) > 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: N maps R \\ {0} to N",
    "¬Q: R is not a Euclidean domain with Euclidean function N"
]

N_HYP = 1
NEG_Q_INDEX = 1