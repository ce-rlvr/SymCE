import sympy

class RingObj:
    def __init__(self, name, has_id, artinian, prod_local):
        self.name = name
        self.has_id = has_id
        self.artinian = artinian
        self.prod_local = prod_local

# Counterexamples: Non-commutative Artinian rings that are NOT products of local rings
M2_R = RingObj("M2_R", True, True, False)
M2_Q = RingObj("M2_Q", True, True, False)
M2_C = RingObj("M2_C", True, True, False)
M2_F2 = RingObj("M2_F2", True, True, False)
M3_R = RingObj("M3_R", True, True, False)

# Non-Artinian matrix ring
M2_Z = RingObj("M2_Z", True, False, False)

# Commutative Artinian rings (These ARE products of local rings)
Z2 = RingObj("Z2", True, True, True)
Z3 = RingObj("Z3", True, True, True)
Z4 = RingObj("Z4", True, True, True)
Z6 = RingObj("Z6", True, True, True)
Z8 = RingObj("Z8", True, True, True)
Q = RingObj("Q", True, True, True)
R = RingObj("R", True, True, True)
C = RingObj("C", True, True, True)

# Commutative non-Artinian rings
Z = RingObj("Z", True, False, False)

# Rings without identity
Z_even = RingObj("Z_even", False, False, False)

def conditions(witness) -> list[bool]:
    if isinstance(witness, str):
        witness = globals().get(witness, witness)
        
    # Handle standard SymPy sets if provided
    if witness == sympy.S.Integers:
        return [True, False, True]
    if witness in (sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
        return [True, True, False]

    try:
        h1_ok = bool(witness.has_id)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(witness.artinian)
    except Exception:
        h2_ok = False

    try:
        # neg_Q is True when the ring is NOT isomorphic to a finite direct product of Artinian local rings
        neg_q_ok = not bool(witness.prod_local)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: R is an Artinian ring",
    "¬Q: R is not isomorphic to a finite direct product of Artinian local rings"
]

N_HYP = 2
NEG_Q_INDEX = 2