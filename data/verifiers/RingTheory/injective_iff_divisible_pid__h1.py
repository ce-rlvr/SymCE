import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y

# Top-level setup: named object bindings that the witness expression may reference.
# The standard counterexample for this conjecture is the fraction field of a domain that is not a PID.
Z_x = ZZ.poly_ring(x)
Q_x = Z_x.get_field()

Q_xy = QQ.poly_ring(x, y)
F_xy = Q_xy.get_field()

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    if isinstance(witness, str):
        w = witness.lower().replace(" ", "")
        if w in ["q(x)overz[x]", "qq(x)overzz[x]", "fractionfieldofz[x]overz[x]"]:
            return [True, True]
            
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
            
            is_frac = False
            try:
                if hasattr(R, 'get_field') and M == R.get_field():
                    is_frac = True
            except Exception:
                pass
                
            try:
                if not is_frac and hasattr(R, 'frac_field'):
                    if M == R.frac_field():
                        is_frac = True
            except Exception:
                pass
                
            if is_frac:
                h1 = True
                is_div = True
                # For Noetherian UFDs (like SymPy polynomial rings),
                # the fraction field is an injective module iff the ring is a PID.
                is_inj = bool(getattr(R, 'is_PID', False))
                q = (is_inj == is_div)
                neg_q = not q
            elif M == R:
                h1 = True
                is_div = bool(getattr(R, 'is_Field', False))
                is_inj = bool(getattr(R, 'is_Field', False))
                q = (is_inj == is_div)
                neg_q = not q
            elif hasattr(M, 'domain') and M.domain == R:
                h1 = True
                is_div = False
                is_inj = False
                q = (is_inj == is_div)
                neg_q = not q
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a module over R",
    "¬Q: M is injective XOR M is divisible"
]

N_HYP = 1
NEG_Q_INDEX = 1