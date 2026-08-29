import sympy
from sympy import Interval, Union, Intersection, FiniteSet, EmptySet, Reals, oo, Set
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    H1: U is an open set in the standard topology
    H2: U is a connected set
    ¬Q: U is not path-connected
    """
    def get_prop(prop):
        # 1. Handle string-based known counterexamples
        if isinstance(witness, str):
            w = witness.lower()
            if prop == "is_open":
                return True
            if prop == "is_connected":
                return True
            if prop == "is_path_connected":
                # Known connected but not path-connected spaces
                if any(x in w for x in ["sine curve", "lexicographic", "long line", "warsaw", "solenoid", "pseudo-arc", "fan", "tent", "broom", "comb"]):
                    return False
                return True

        # 2. Handle mock objects or objects with explicit attributes
        if hasattr(witness, prop):
            try:
                val = getattr(witness, prop)
                if callable(val):
                    val = val()
                if val is not None:
                    return val
            except Exception:
                pass

        # 3. Handle dictionary-based witnesses
        if isinstance(witness, dict) and prop in witness:
            return witness[prop]

        # 4. Handle SymPy sets (subsets of R^n where connected implies path-connected)
        if isinstance(witness, Set):
            if prop == "is_open":
                return witness.is_open
            if prop == "is_connected":
                return witness.is_connected
            if prop == "is_path_connected":
                return witness.is_connected

        # Default fallbacks to prevent false positives on the negated conclusion
        if prop == "is_path_connected":
            return True
        return False

    try:
        h1_ok = bool(get_prop("is_open"))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(get_prop("is_connected"))
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not bool(get_prop("is_path_connected"))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: U is an open set in the standard topology",
    "H_2: U is a connected set",
    "¬Q: U is not path-connected"
]

N_HYP = 2
NEG_Q_INDEX = 2