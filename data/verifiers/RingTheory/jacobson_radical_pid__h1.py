import sympy
from sympy.ntheory import factorint

class CustomRing:
    def __init__(self, inf_max, jacobson_zero):
        self.inf_max = inf_max
        self.jacobson_zero = jacobson_zero

# Standard counterexamples that might be referenced by the witness
Z_formal_power_series = CustomRing(True, False)
Z_times_Z4 = CustomRing(True, False)

def has_infinitely_many_maximal_ideals(R):
    if isinstance(R, (tuple, list)):
        return any(has_infinitely_many_maximal_ideals(r) for r in R)
    if hasattr(R, 'inf_max'):
        return R.inf_max
    if isinstance(R, int):
        if R == 0:
            return True
        return False
    if isinstance(R, str):
        R_str = R.replace(" ", "")
        if "[[x]]" in R_str:
            if "Z_p" in R_str or "Q" in R_str:
                return False
            if "Z" in R_str:
                return True
        if "[x]" in R_str:
            return True
        if R_str in ["Z", "ZZ"]:
            return True
        if R_str in ["Q", "QQ", "R", "C"]:
            return False
        if R_str in ["Z2", "Z3", "Z4", "Z6", "Z8", "Z9"]:
            return False
    if R == sympy.ZZ:
        return True
    if R == sympy.QQ:
        return False
    if hasattr(R, 'domain'):
        return True
    return False

def jacobson_radical_is_zero(R):
    if isinstance(R, (tuple, list)):
        return all(jacobson_radical_is_zero(r) for r in R)
    if hasattr(R, 'jacobson_zero'):
        return R.jacobson_zero
    if isinstance(R, int):
        if R == 0:
            return True
        if R in (1, -1):
            return True
        factors = factorint(abs(R))
        return all(v == 1 for v in factors.values())
    if isinstance(R, str):
        R_str = R.replace(" ", "")
        if "[[x]]" in R_str:
            return False
        if "[x]" in R_str:
            return True
        if R_str in ["Z", "ZZ", "Q", "QQ", "R", "C"]:
            return True
        if R_str in ["Z2", "Z3", "Z6"]:
            return True
        if R_str in ["Z4", "Z8", "Z9"]:
            return False
    if R == sympy.ZZ:
        return True
    if R == sympy.QQ:
        return True
    if hasattr(R, 'domain'):
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(has_infinitely_many_maximal_ideals(witness))
    except Exception:
        h1 = False
        
    try:
        # The conclusion is "The Jacobson radical of R is the zero ideal."
        # We want neg_Q to be True when the conclusion FAILS.
        neg_q = not bool(jacobson_radical_is_zero(witness))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R has infinitely many distinct maximal ideals",
    "¬Q: The Jacobson radical of R is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1