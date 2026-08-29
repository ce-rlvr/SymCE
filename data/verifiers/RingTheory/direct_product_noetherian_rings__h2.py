import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from sympy.polys.domains import ZZ, QQ, RR, CC
import itertools

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

def is_noetherian(R):
    """Helper to check if a given ring/domain is Noetherian."""
    if R in [ZZ, QQ, RR, CC]:
        return True
    if hasattr(R, 'is_Field') and getattr(R, 'is_Field'):
        return True
    if hasattr(R, 'is_Noetherian') and getattr(R, 'is_Noetherian'):
        return True
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        # Polynomial ring over a domain
        return is_noetherian(R.domain)
    if isinstance(R, str) and R.upper() in ['Z', 'Q', 'R', 'C', 'ZZ', 'QQ', 'RR', 'CC']:
        return True
    if hasattr(R, 'is_FiniteField') and getattr(R, 'is_FiniteField'):
        return True
    return False

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the conjecture:
    H1: Let n be a positive integer.
    H2: Each ring R_i is a Noetherian ring.
    Q: The direct product ring R_1 x R_2 x ... x R_n is a Noetherian ring.
    """
    # Parse witness: expect either (n, rings) or just rings
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
            n, rings = witness
        else:
            rings = witness
            n = len(rings) if hasattr(rings, '__len__') else None
    except Exception:
        n = None
        rings = []

    # H_1: n is a positive integer
    try:
        h1_ok = isinstance(n, int) and n > 0
    except Exception:
        h1_ok = False

    # H_2: Each ring R_i is a Noetherian ring
    try:
        if hasattr(rings, '__iter__'):
            if not hasattr(rings, '__len__'):
                # Prevent infinite loops by checking a sample
                rings_sample = list(itertools.islice(rings, 1000))
                h2_ok = all(is_noetherian(r) for r in rings_sample)
            else:
                h2_ok = all(is_noetherian(r) for r in rings)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The direct product ring R_1 x R_2 x ... x R_n is NOT a Noetherian ring
    try:
        # A finite direct product of rings is Noetherian if and only if each factor is Noetherian.
        if isinstance(n, int) and n > 0:
            if hasattr(rings, '__iter__'):
                if not hasattr(rings, '__len__'):
                    rings_sample = list(itertools.islice(rings, 1000))
                    prod_noetherian = all(is_noetherian(r) for r in rings_sample)
                else:
                    prod_noetherian = all(is_noetherian(r) for r in rings)
            else:
                prod_noetherian = False
        else:
            prod_noetherian = False
            
        neg_q_ok = not prod_noetherian
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: Each ring R_i is a Noetherian ring",
    "¬Q: The direct product ring R_1 x R_2 x ... x R_n is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2