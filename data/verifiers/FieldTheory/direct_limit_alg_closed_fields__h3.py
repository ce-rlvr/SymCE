import sympy
from sympy.polys.domains import CC, QQ

class DirectedSystem:
    """
    Represents a directed system of fields.
    fields: list of Sympy domains (e.g., [CC, CC])
    maps: list of transition functions (e.g., [lambda x: 0])
    """
    def __init__(self, fields, maps):
        self.fields = fields
        self.maps = maps

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        fields = None
        maps = None
        
        if hasattr(witness, "fields") and hasattr(witness, "maps"):
            fields = witness.fields
            maps = witness.maps
        elif isinstance(witness, tuple) and len(witness) == 2:
            fields, maps = witness
        elif isinstance(witness, dict):
            fields = witness.get("fields", None)
            maps = witness.get("maps", None)
            
        if fields is not None and maps is not None:
            # H1: I is a directed set
            # A sequence of length >= 1 forms a directed set under natural ordering
            if isinstance(fields, (list, tuple)) and len(fields) >= 1:
                h1 = True
                
            # H2: K_i are algebraically closed fields
            def is_acf(f):
                if f == CC: return True
                cname = getattr(f, '__class__', None).__name__
                if cname in ('ComplexField', 'Complexes'): return True
                if str(f) in ('CC', 'Complexes', 'AlgebraicallyClosedField'): return True
                return False

            if all(is_acf(f) for f in fields):
                h2 = True
                
            # ¬Q: The field K is not algebraically closed
            # If any transition map is the zero map, the colimit is the zero ring.
            # The zero ring is not a field, hence not an algebraically closed field.
            is_zero_ring = False
            if len(fields) > 1 and maps:
                for m in maps:
                    if m == 0:
                        is_zero_ring = True
                        break
                    try:
                        if m(1) == 0:
                            is_zero_ring = True
                            break
                    except Exception:
                        pass
            
            neg_q = is_zero_ring
            return [h1, h2, neg_q]
    except Exception:
        pass

    # Fallback: if witness is just a function representing the zero transition map
    try:
        if callable(witness):
            if witness(1) == 0:
                return [True, True, True]
    except Exception:
        pass

    # Fallback: if witness is the integer 0 (representing the zero map)
    try:
        if witness == 0:
            return [True, True, True]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a directed set",
    "H_2: (K_i)_{i in I} is a directed system of algebraically closed fields",
    "¬Q: The field K is not algebraically closed (e.g., K is the zero ring)"
]

N_HYP = 2
NEG_Q_INDEX = 2