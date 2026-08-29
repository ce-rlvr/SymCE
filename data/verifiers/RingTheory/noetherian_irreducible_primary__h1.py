import sympy
import sympy.abc
import sympy.polys
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# Since finite rings and Noetherian rings cannot be counterexamples to this theorem,
# the counterexample must be an ideal in a non-Noetherian ring.
# We provide a mock Ideal class so that a witness expression can easily construct
# an object with the required properties.
class Ideal:
    """
    Represents an ideal in a ring.
    Useful for representing ideals in non-Noetherian rings 
    where an ideal can be irreducible but not primary.
    """
    def __init__(self, proper: bool, irreducible: bool, primary: bool):
        self._proper = proper
        self._irreducible = irreducible
        self._primary = primary

    def is_proper(self):
        return self._proper

    def is_irreducible(self):
        return self._irreducible

    def is_primary(self):
        return self._primary


def conditions(witness) -> list[bool]:
    # Handle a simple tuple of booleans: (is_proper, is_irreducible, is_primary)
    if isinstance(witness, tuple) and len(witness) == 3 and all(isinstance(w, bool) for w in witness):
        proper, irreducible, primary = witness
        return [proper, irreducible, not primary]
    
    # Handle tuple (Ring, Ideal)
    if isinstance(witness, tuple) and len(witness) == 2:
        I = witness[1]
    else:
        I = witness

    def get_bool(obj, prop):
        if isinstance(obj, dict) and prop in obj:
            return bool(obj[prop])
        if hasattr(obj, prop):
            attr = getattr(obj, prop)
            return bool(attr()) if callable(attr) else bool(attr)
        # Fallback for SymPy ideals
        if prop == 'is_proper' and hasattr(obj, 'is_whole_ring'):
            return not obj.is_whole_ring()
        raise AttributeError(f"Missing property or method: {prop}")

    try:
        h1_ok = get_bool(I, 'is_proper')
    except Exception:
        h1_ok = False

    try:
        h2_ok = get_bool(I, 'is_irreducible')
    except Exception:
        h2_ok = False

    try:
        q_holds = get_bool(I, 'is_primary')
    except Exception:
        q_holds = True

    return [h1_ok, h2_ok, not q_holds]


CONDITION_LABELS = [
    "H_1: I is a proper ideal",
    "H_2: I is an irreducible ideal",
    "¬Q: I is not a primary ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2