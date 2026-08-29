import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

def _get_prop(witness, prop_names):
    """Helper to extract boolean properties from a dictionary or mock object."""
    if isinstance(witness, dict):
        for p in prop_names:
            if p in witness:
                return bool(witness[p])
    else:
        for p in prop_names:
            if hasattr(witness, p):
                return bool(getattr(witness, p))
    raise ValueError(f"Property not found: {prop_names}")

def conditions(witness) -> list[bool]:
    # H_1: 0 \to L \to M \to N \to 0 is a short exact sequence of R-modules
    try:
        h1 = _get_prop(witness, ['is_short_exact_sequence', 'is_exact', 'exact_sequence'])
    except Exception:
        h1 = False

    # ¬Q: The module M is Noetherian if and only if both L and N are Noetherian modules.
    try:
        m_noeth = _get_prop(witness, ['M_is_noetherian', 'm_noetherian', 'M_noetherian'])
        l_noeth = _get_prop(witness, ['L_is_noetherian', 'l_noetherian', 'L_noetherian'])
        n_noeth = _get_prop(witness, ['N_is_noetherian', 'n_noetherian', 'N_noetherian'])
        
        # Q is True if M is Noetherian exactly when both L and N are Noetherian
        q = (m_noeth == (l_noeth and n_noeth))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: 0 -> L -> M -> N -> 0 is a short exact sequence of R-modules",
    "¬Q: It is not the case that M is Noetherian iff both L and N are Noetherian"
]

N_HYP = 1
NEG_Q_INDEX = 1