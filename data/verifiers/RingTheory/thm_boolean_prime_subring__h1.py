import sympy
from sympy import ZZ, QQ
from sympy.polys.domains import GF

# Top-level setup: named object bindings that the witness expression may reference.
# We use integers to represent the ring Z/nZ (with 0 representing Z).
Z2 = 2
Z3 = 3
Z4 = 4
Z6 = 6
trivial = 1

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be a ring with identity 1 != 0. Let P be the prime subring of R. 
    Then P is isomorphic to Z/2Z."
    """
    
    # H_1: R has an identity element 1 != 0
    h1 = False
    try:
        if isinstance(witness, int):
            # For Z/nZ, 1 != 0 iff n != 1
            h1 = (witness >= 0 and witness != 1)
        elif hasattr(witness, 'is_Ring') and witness.is_Ring:
            h1 = bool(witness.zero != witness.one)
        elif witness in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h1 = True
    except Exception:
        pass

    # H_2: P is the prime subring of R
    # This is a definitional hypothesis that holds for any valid ring.
    h2 = False
    try:
        if isinstance(witness, int):
            h2 = (witness >= 0)
        elif hasattr(witness, 'is_Ring') and witness.is_Ring:
            h2 = True
        elif witness in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h2 = True
    except Exception:
        pass

    # neg_Q: P is not isomorphic to Z/2Z
    # The prime subring P is isomorphic to Z/2Z iff the characteristic of R is 2.
    neg_q = False
    try:
        if isinstance(witness, int):
            char = witness
            neg_q = (char != 2)
        elif hasattr(witness, 'characteristic'):
            char = witness.characteristic()
            neg_q = (char != 2)
        elif witness in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            neg_q = True  # Characteristic is 0
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R has an identity element 1 != 0",
    "H_2: P is the prime subring of R",
    "¬Q: P is not isomorphic to Z/2Z"
]

N_HYP = 2
NEG_Q_INDEX = 2