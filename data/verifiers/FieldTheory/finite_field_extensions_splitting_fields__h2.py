import sympy
from sympy.ntheory import factorint
from sympy import GF

# Top-level setup
# Witnesses are expected to be tuples (q, n, E_order) or dicts with these keys.
# SymPy's GF can be used to construct finite fields if desired.

def get_order(obj):
    """Helper to extract the order from a finite field object or return the integer."""
    if hasattr(obj, 'order'):
        val = obj.order
        if callable(val):
            return val()
        return val
    if hasattr(obj, 'mod'):
        return obj.mod
    return int(obj)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            q = witness.get('q', witness.get('F', 0))
            n = witness.get('n', 0)
            E_order = witness.get('E_order', witness.get('E', 0))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                q, n, E_order = witness
            else:
                return [False, False]
        else:
            return [False, False]
            
        q = get_order(q)
        n = int(n)
        E_order = get_order(E_order)
    except Exception:
        return [False, False]
        
    # H_1: F is a finite field of order q
    # This means q must be a prime power (order of a valid finite field)
    try:
        factors_q = factorint(q)
        h1 = (q >= 2) and (len(factors_q) == 1)
    except Exception:
        h1 = False
        
    # ¬Q: E is NOT the splitting field of x^{q^n} - x over F
    # The splitting field of x^{q^n} - x over F (where F has order q)
    # is the unique finite field of order q^n.
    # So E is the splitting field iff E is a finite field of order q^n
    # and has the same characteristic as F.
    try:
        if E_order < 2:
            neg_q = True
        else:
            factors_E = factorint(E_order)
            is_field_E = (len(factors_E) == 1)
            if not is_field_E:
                neg_q = True
            else:
                char_F = list(factors_q.keys())[0] if h1 else 0
                char_E = list(factors_E.keys())[0]
                
                if char_F != char_E:
                    neg_q = True
                elif E_order != q**n:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "¬Q: E is not the splitting field of x^{q^n} - x over F"
]

N_HYP = 1
NEG_Q_INDEX = 1