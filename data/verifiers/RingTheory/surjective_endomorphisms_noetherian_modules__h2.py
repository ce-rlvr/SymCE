import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    Hypotheses:
      1. R is a ring
      2. f: M -> M is a surjective R-module homomorphism
    Conclusion:
      f is an isomorphism
    """
    def get_prop(prop_name, default=False):
        try:
            if isinstance(witness, dict):
                if prop_name in witness:
                    val = witness[prop_name]
                else:
                    return default
            else:
                if hasattr(witness, prop_name):
                    val = getattr(witness, prop_name)
                else:
                    return default
            if callable(val):
                return bool(val())
            return bool(val)
        except Exception:
            return default

    try:
        h1 = get_prop('is_ring', False)
    except Exception:
        h1 = False

    try:
        is_module = get_prop('is_module', True)
        is_hom = get_prop('is_homomorphism', False)
        is_surj = get_prop('is_surjective', False)
        h2 = is_module and is_hom and is_surj
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict) and 'is_isomorphism' in witness:
            is_iso = get_prop('is_isomorphism')
        elif hasattr(witness, 'is_isomorphism'):
            is_iso = get_prop('is_isomorphism')
        else:
            is_inj = get_prop('is_injective', True)
            is_iso = get_prop('is_homomorphism', False) and get_prop('is_surjective', False) and is_inj
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: f: M \\to M is a surjective R-module homomorphism",
    "¬Q: The homomorphism f is not an isomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2