import sympy
import sympy.polys
from sympy.abc import x, y, z

# Top-level setup
ZZ = sympy.polys.domains.ZZ
QQ = sympy.polys.domains.QQ

class LocalPID:
    """A local principal ideal domain (e.g., a discrete valuation ring)."""
    is_PID = True
    jacobson_radical_is_zero = False
    
    def __init__(self, name="R"):
        self.name = name
        
    def __str__(self):
        return self.name

class FormalPowerSeriesRing(LocalPID):
    """Formal power series ring k[[x]], which is a DVR."""
    pass

class PAdicIntegers(LocalPID):
    """Ring of p-adic integers, which is a DVR."""
    pass

Z_p = LocalPID("Z_{(p)}")
k_x = FormalPowerSeriesRing("k[[x]]")

def check_is_pid(w):
    if isinstance(w, dict):
        if "is_PID" in w: return w["is_PID"]
        if "is_pid" in w: return w["is_pid"]
    if isinstance(w, str):
        w_lower = w.lower()
        if "[[" in w and "]]" in w: return True
        if "z_(" in w_lower or "localization" in w_lower: return True
        if "z_p" in w_lower or "padic" in w_lower or "p-adic" in w_lower: return True
        if "dvr" in w_lower or "discrete valuation" in w_lower: return True
        if "local pid" in w_lower: return True
        if w_lower in ["z", "q", "r", "c"]: return True
    if hasattr(w, 'is_PID'):
        val = w.is_PID
        return val() if callable(val) else val
    if hasattr(w, 'is_pid'):
        val = w.is_pid
        return val() if callable(val) else val
    return False

def check_jacobson_radical_is_zero(w):
    if isinstance(w, dict):
        if "jacobson_radical_is_zero" in w: return w["jacobson_radical_is_zero"]
        if "jacobson_radical" in w:
            res = w["jacobson_radical"]
            return res == 0 or res == "0" or res == "zero"
    if isinstance(w, str):
        w_lower = w.lower()
        if "[[" in w and "]]" in w: return False
        if "z_(" in w_lower or "localization" in w_lower: return False
        if "z_p" in w_lower or "padic" in w_lower or "p-adic" in w_lower: return False
        if "dvr" in w_lower or "discrete valuation" in w_lower: return False
        if "local pid" in w_lower: return False
        if w_lower in ["z", "q", "r", "c"]: return True
    if hasattr(w, 'jacobson_radical_is_zero'):
        val = w.jacobson_radical_is_zero
        return val() if callable(val) else val
    if hasattr(w, 'jacobson_radical'):
        val = w.jacobson_radical
        res = val() if callable(val) else val
        return res == 0 or res == "0" or res == "zero"
    return True

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(check_is_pid(witness))
    except Exception:
        h1 = False
        
    try:
        neg_q = not bool(check_jacobson_radical_is_zero(witness))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: The Jacobson radical of R is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1