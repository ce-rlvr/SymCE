import sympy
from sympy import Symbol

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy does not natively represent non-UFD integral domains easily, 
# we provide mock objects for the most common counterexamples.
class Ring:
    def __init__(self, name, is_id, is_ufd):
        self.name = name
        self.is_integral_domain = is_id
        self.is_ufd = is_ufd
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

Z_sqrt_minus_5 = Ring("Z[sqrt(-5)]", True, False)
Z_sqrt_minus_3 = Ring("Z[sqrt(-3)]", True, False)
Z_sqrt_minus_6 = Ring("Z[sqrt(-6)]", True, False)
Z_i = Ring("Z[i]", True, True)
Z = Ring("Z", True, True)
Q = Ring("Q", True, True)
Z6 = Ring("Z6", False, False)
Z4 = Ring("Z4", False, False)

def get_ring_properties(w):
    """
    Helper function to determine if the witness is an integral domain and a UFD.
    Returns a tuple (is_integral_domain, is_ufd).
    """
    # 1. Check if it's one of our predefined mock rings
    if isinstance(w, Ring):
        return (w.is_integral_domain, w.is_ufd)
        
    # 2. Check if it's a custom object with the right attributes
    if hasattr(w, 'is_integral_domain') and hasattr(w, 'is_ufd'):
        try:
            return (bool(w.is_integral_domain), bool(w.is_ufd))
        except Exception:
            pass
            
    # 3. Check if it's a string or a SymPy Symbol representing a known ring
    name = ""
    if isinstance(w, str):
        name = w
    elif hasattr(w, 'name') and isinstance(w.name, str):
        name = w.name
        
    if name:
        name = name.replace(" ", "").lower()
        # Known integral domains that are NOT UFDs
        if any(sub in name for sub in ["sqrt(-5)", "sqrt(-3)", "sqrt(-6)", "sqrt(-10)", 
                                       "sqrt_minus_5", "sqrt_minus_3", "sqrt_minus_6", 
                                       "x^2,x^3", "x**2,x**3", "xy-zw"]):
            return (True, False)
        # Known integral domains that ARE UFDs
        if name in ["z", "q", "r", "c", "z[x]", "z[i]", "zz", "qq"]:
            return (True, True)
        # Known rings that are NOT integral domains
        if name in ["z6", "z4", "z/6z", "z/4z"]:
            return (False, False)
            
    # 4. Check if it's a SymPy domain
    if w in [sympy.ZZ, sympy.QQ]:
        return (True, True)
        
    if hasattr(w, 'is_UFD'):
        try:
            is_ufd = bool(w.is_UFD)
            # In SymPy, domains that implement is_UFD are integral domains
            return (True, is_ufd)
        except Exception:
            pass
            
    # Default fallback if we cannot determine the properties
    return (False, False)

def conditions(witness) -> list[bool]:
    try:
        is_id, is_ufd = get_ring_properties(witness)
    except Exception:
        is_id, is_ufd = False, False
        
    return [is_id, not is_ufd]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: R is not a unique factorization domain"
]

N_HYP = 1
NEG_Q_INDEX = 1