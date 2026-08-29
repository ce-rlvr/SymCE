import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
# Non-commutative symbols in case the witness is constructed via free algebras
nc_x, nc_y, nc_z = symbols('x y z', commutative=False)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be an object (or dictionary) representing the ideal I,
    or a tuple (R, I) where I is the ideal.
    """
    # Extract the ideal object if a tuple (R, I) is provided
    if isinstance(witness, tuple) and len(witness) == 2:
        obj = witness[1]
    else:
        obj = witness

    def check_property(prop_names, default=False):
        if isinstance(obj, dict):
            for p in prop_names:
                if p in obj:
                    val = obj[p]
                    return bool(val() if callable(val) else val)
        for p in prop_names:
            if hasattr(obj, p):
                val = getattr(obj, p)
                return bool(val() if callable(val) else val)
        return default

    # H_1: Let I be a finitely generated ideal of R.
    try:
        h1_ok = check_property(["is_finitely_generated_ideal", "is_finitely_generated"])
    except Exception:
        h1_ok = False

    # H_2: Let every element of I be nilpotent (i.e., I is a nil ideal).
    try:
        h2_ok = check_property(["is_nil_ideal", "is_nil"])
    except Exception:
        h2_ok = False

    # ¬Q: There does NOT exist a positive integer n such that I^n = 0.
    # (i.e., I is NOT a nilpotent ideal).
    try:
        is_nilpotent = check_property(["is_nilpotent_ideal", "is_nilpotent"], default=None)
        if is_nilpotent is not None:
            neg_q_ok = not is_nilpotent
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is a finitely generated ideal of R",
    "H_2: Every element of I is nilpotent",
    "¬Q: There does not exist a positive integer n such that I^n = 0"
]

N_HYP = 2
NEG_Q_INDEX = 2