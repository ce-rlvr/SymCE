import sympy
from sympy.polys.domains import QQ, ZZ
from sympy.abc import x, y, z

def is_frac_field_of(M, R):
    try:
        from sympy.polys.rings import PolyRing
        from sympy.polys.fields import FracField
        if isinstance(R, PolyRing) and isinstance(M, FracField):
            if hasattr(M, 'ring') and M.ring == R:
                return True
            if M.gens == R.gens and M.domain == R.domain:
                return True
    except Exception:
        pass
    return False

def parse_witness(witness):
    R, M = None, None
    if isinstance(witness, tuple) and len(witness) == 2:
        R, M = witness
    elif isinstance(witness, dict):
        R = witness.get('R', witness.get('r', witness.get('ring')))
        M = witness.get('M', witness.get('m', witness.get('module')))
    elif isinstance(witness, str):
        R = witness
        M = witness
    else:
        # Assume witness is the ring R, and M is implicitly its fraction field
        R = witness
        M = "implicit_frac_field"
    return R, M

def is_divisible(R, M):
    if R is None or M is None:
        return False
        
    if M == "implicit_frac_field":
        if hasattr(R, 'is_domain') and R.is_domain:
            return True
        try:
            from sympy.polys.rings import PolyRing
            if isinstance(R, PolyRing):
                return True
        except Exception:
            pass
        return False
        
    try:
        if hasattr(R, 'is_domain') and R.is_domain:
            if hasattr(R, 'get_field') and R.get_field() == M:
                return True
    except Exception:
        pass
        
    if is_frac_field_of(M, R):
        return True
        
    if isinstance(R, str):
        s = R.lower().replace(" ", "").replace("\\mathbb", "").replace("{", "").replace("}", "")
        if "[" in s and "]" in s:
            return True
        if s in ["z", "zz", "q", "qq", "r", "c"]:
            return True
            
    return False

def is_injective(R, M):
    if R is None or M is None:
        return True
        
    if M == "implicit_frac_field":
        try:
            from sympy.polys.rings import PolyRing
            if isinstance(R, PolyRing):
                n_vars = len(R.gens)
                if R.domain.is_Field:
                    return n_vars <= 1
                else:
                    return n_vars == 0
        except Exception:
            pass
        if hasattr(R, 'is_PID'):
            return R.is_PID
        return True
        
    if is_frac_field_of(M, R):
        try:
            n_vars = len(R.gens)
            if R.domain.is_Field:
                return n_vars <= 1
            else:
                return n_vars == 0
        except Exception:
            pass
            
    try:
        if hasattr(R, 'get_field') and R.get_field() == M:
            if hasattr(R, 'is_PID'):
                return R.is_PID
    except Exception:
        pass
        
    if isinstance(R, str):
        s = R.lower().replace(" ", "").replace("\\mathbb", "").replace("{", "").replace("}", "")
        if "[" in s and "]" in s:
            vars_part = s.split("[")[1].split("]")[0]
            if "," in vars_part:
                return False
            if s.startswith("z[") or s.startswith("zz["):
                return False
            return True
            
    return True

def conditions(witness):
    R, M = parse_witness(witness)
    
    try:
        h1 = is_divisible(R, M)
    except Exception:
        h1 = False
        
    try:
        q = is_injective(R, M)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: M is a divisible module over R",
    "¬Q: M is not an injective R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1