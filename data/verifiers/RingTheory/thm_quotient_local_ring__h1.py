import sympy
from sympy.ntheory import factorint

# Top-level setup: named object bindings that the witness expression may reference.
# We interpret the witness as an integer n, representing the ideal nZ in the ring of integers Z.
Z = "Ring of Integers"
ZZ = sympy.ZZ

def parse_witness(witness):
    """
    Helper to extract the integer generator n of the ideal nZ.
    """
    if isinstance(witness, int):
        return witness
    if hasattr(witness, 'is_Integer') and witness.is_Integer:
        return int(witness)
    if isinstance(witness, (tuple, list, set)):
        for item in witness:
            if isinstance(item, int):
                return item
            if hasattr(item, 'is_Integer') and item.is_Integer:
                return int(item)
    return int(witness)

def conditions(witness) -> list[bool]:
    try:
        n = parse_witness(witness)
        # H_1: I is a proper ideal of R
        # In Z, the ideal nZ is proper if and only if n != 1 and n != -1.
        h1_ok = bool(abs(n) != 1)
    except Exception:
        h1_ok = False

    try:
        n = parse_witness(witness)
        # ¬Q: R/I is NOT a local ring
        # A ring is local if it has exactly one maximal ideal.
        if n == 0:
            # Z/0Z is isomorphic to Z, which has infinitely many maximal ideals.
            neg_q_ok = True
        elif abs(n) == 1:
            # Z/1Z is the zero ring, which has 0 maximal ideals.
            neg_q_ok = True
        else:
            # For n > 1, Z/nZ has maximal ideals corresponding to the distinct prime factors of n.
            # It is a local ring if and only if it has exactly one distinct prime factor.
            factors = factorint(abs(n))
            is_local = (len(factors) == 1)
            neg_q_ok = not is_local
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: R/I is not a local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1