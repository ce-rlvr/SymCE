import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup
from sympy.ntheory import factorint

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_field(F):
    """Check if F represents a field."""
    if isinstance(F, int):
        if F < 2:
            return False
        # A finite field exists iff its size is a prime power
        return len(factorint(F)) == 1
    if hasattr(F, 'is_Field'):
        return F.is_Field
    if hasattr(F, 'is_field'):
        return F.is_field
    if str(F) in ['Q', 'R', 'C', 'QQ', 'RR', 'CC']:
        return True
    return False

def get_order(F):
    """Get the order of the field F."""
    if isinstance(F, int):
        return F
    if hasattr(F, 'order'):
        try:
            return int(F.order)
        except Exception:
            pass
    return float('inf')

def conditions(witness) -> list[bool]:
    n = None
    F = None
    
    # Parse the witness
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            F = witness.get('F')
        elif isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], int) and not isinstance(witness[1], int):
                n, F = witness
            elif isinstance(witness[1], int) and not isinstance(witness[0], int):
                F, n = witness
            else:
                # If both are ints, assume (n, q)
                n, F = witness
    except Exception:
        pass

    # H_1: Let F be a field
    try:
        h1 = is_field(F)
    except Exception:
        h1 = False

    # H_2: Let n be a positive integer
    try:
        h2 = isinstance(n, int) and n >= 1
    except Exception:
        h2 = False

    # H_3: Assume that either n >= 3, or both n = 2 and |F| > 3
    try:
        if not h2:
            h3 = False
        else:
            order = get_order(F)
            h3 = (n >= 3) or (n == 2 and order > 3)
    except Exception:
        h3 = False

    # H_4: Let SL_n(F) be the special linear group of degree n over F
    # This is a definitional hypothesis. It holds if n and F are valid.
    try:
        h4 = h1 and h2
    except Exception:
        h4 = False

    # ¬Q: The commutator subgroup of GL_n(F) is NOT SL_n(F)
    # Mathematically, the commutator subgroup of GL_n(F) is SL_n(F) for all fields
    # and all n >= 1, EXCEPT when n = 2 and |F| = 2 (where it is A_3 instead of S_3).
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            order = get_order(F)
            neg_q = (n == 2 and order == 2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is a positive integer",
    "H_3: either n >= 3, or both n = 2 and |F| > 3",
    "H_4: SL_n(F) is the special linear group of degree n over F",
    "¬Q: The commutator subgroup of GL_n(F) is not SL_n(F)"
]

N_HYP = 4
NEG_Q_INDEX = 4