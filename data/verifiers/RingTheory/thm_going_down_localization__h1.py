import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def extract_bool(witness, names, default):
    if isinstance(witness, dict):
        for name in names:
            if name in witness:
                return bool(witness[name])
    else:
        for name in names:
            if hasattr(witness, name):
                val = getattr(witness, name)
                return bool(val() if callable(val) else val)
    return default

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for any ring R and multiplicative subset S, 
    the canonical homomorphism phi: R -> S^{-1}R satisfies the going-down theorem.
    (This is true for commutative rings, but fails in general for non-commutative rings).
    """
    # Handle case where witness is a callable that returns the properties
    if callable(witness):
        try:
            witness = witness()
        except Exception:
            pass

    # Handle case where witness is a simple tuple/list of booleans: (H1, H2, Q)
    if isinstance(witness, (list, tuple)) and len(witness) == 3:
        try:
            return [bool(witness[0]), bool(witness[1]), not bool(witness[2])]
        except Exception:
            pass

    # Possible attribute/key names for the hypotheses and conclusion
    h1_names = ['S_is_multiplicative_subset', 'is_multiplicative_subset', 'multiplicative_subset', 'is_multiplicative', 'h1']
    h2_names = ['phi_is_canonical_homomorphism', 'is_canonical_homomorphism', 'canonical_homomorphism', 'is_canonical', 'h2']
    q_names = ['satisfies_going_down', 'going_down_theorem', 'is_going_down', 'satisfies_going_down_property', 'q']

    try:
        h1_ok = extract_bool(witness, h1_names, False)
    except Exception:
        h1_ok = False

    try:
        h2_ok = extract_bool(witness, h2_names, False)
    except Exception:
        h2_ok = False

    try:
        # q_ok is True if the conclusion HOLDS. We want it to FAIL.
        q_ok = extract_bool(witness, q_names, True)
    except Exception:
        q_ok = True

    return [h1_ok, h2_ok, not q_ok]

CONDITION_LABELS = [
    "H_1: S is a multiplicative subset of R",
    "H_2: phi is the canonical ring homomorphism",
    "¬Q: The map phi does not satisfy the going-down theorem"
]

N_HYP = 2
NEG_Q_INDEX = 2