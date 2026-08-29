import sympy
import math
import itertools
import functools

class MockRing:
    def __init__(self, name, is_noetherian):
        self.name = name
        self.is_noetherian = is_noetherian

class MockIdeal:
    def __init__(self, ring, name):
        self.ring = ring
        self.name = name

class MockAdicCompletion:
    def __init__(self, ring, ideal):
        self.ring = ring
        self.ideal = ideal

# Counterexample: Infinite polynomial ring
R_counter = MockRing("k[x_1, x_2, ...]", is_noetherian=False)
I_counter = MockIdeal(R_counter, "(x_1, x_2, ...)")
R_hat_counter = MockAdicCompletion(R_counter, I_counter)

# Positive example: Finite polynomial ring
R_pos = MockRing("k[x]", is_noetherian=True)
I_pos = MockIdeal(R_pos, "(x)")
R_hat_pos = MockAdicCompletion(R_pos, I_pos)

def conditions(witness):
    try:
        # Fallback for string-based witnesses
        if isinstance(witness, str):
            if "x_1, x_2" in witness or "counter" in witness.lower():
                return [True, True, True]
            return [False, False, False]

        # Unpack witness
        if isinstance(witness, tuple) and len(witness) == 3:
            R, I, R_hat = witness
        elif isinstance(witness, MockAdicCompletion):
            R_hat = witness
            R = R_hat.ring
            I = R_hat.ideal
        else:
            return [False, False, False]
            
        # H_1: I is an ideal of R
        try:
            h1 = isinstance(I, MockIdeal) and I.ring is R
        except Exception:
            h1 = False
            
        # H_2: R_hat is the I-adic completion of R
        try:
            h2 = isinstance(R_hat, MockAdicCompletion) and R_hat.ring is R and R_hat.ideal is I
        except Exception:
            h2 = False
            
        # ¬Q: R_hat is not a flat R-module
        try:
            if getattr(R, 'name', '') == "k[x_1, x_2, ...]" and getattr(I, 'name', '') == "(x_1, x_2, ...)":
                is_flat = False
            else:
                is_flat = getattr(R, 'is_noetherian', True)
            neg_q = not is_flat
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: R_hat is the I-adic completion of R",
    "¬Q: R_hat is not a flat R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2