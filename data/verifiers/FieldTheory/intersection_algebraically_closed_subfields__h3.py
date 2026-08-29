import sympy

# Top-level setup: named object bindings for Field Theory
class MyField:
    def __init__(self, name, elements, is_alg_closed):
        self.name = name
        self.elements = frozenset(elements)
        self.is_alg_closed = is_alg_closed

    def __repr__(self):
        return self.name

# Define standard fields with their element signatures to easily compute intersections
Q = MyField("Q", {"q"}, False)
R = MyField("R", {"q", "t"}, False)
Qbar = MyField("Qbar", {"q", "a"}, True)
C = MyField("C", {"q", "t", "a", "c"}, True)

Fp = MyField("Fp", {"fp"}, False)
Fpbar = MyField("Fpbar", {"fp", "fpa"}, True)

# Aliases for common notation
QQ = Q
RR = R
CC = C
QQbar = Qbar

ALL_FIELDS = [Q, R, Qbar, C, Fp, Fpbar]

def get_field_by_elements(elements):
    for f in ALL_FIELDS:
        if f.elements == elements:
            return f
    return None

def conditions(witness) -> list[bool]:
    try:
        E, K_family = witness
    except Exception:
        return [False, False, False]
    
    # H_1: E is a field
    try:
        h1 = isinstance(E, MyField)
    except Exception:
        h1 = False
        
    # H_2: {K_i} is a non-empty family of subfields of E
    try:
        K_family = list(K_family)
        if len(K_family) > 0:
            h2 = all(isinstance(k, MyField) and k.elements.issubset(E.elements) for k in K_family)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: The intersection of {K_i} is NOT an algebraically closed subfield of E
    try:
        if not h2:
            neg_q = False
        else:
            intersect_elems = set(K_family[0].elements)
            for k in K_family[1:]:
                intersect_elems &= set(k.elements)
                
            intersect_field = get_field_by_elements(intersect_elems)
            
            if intersect_field is None:
                neg_q = False
            else:
                neg_q = not intersect_field.is_alg_closed
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is a field",
    "H_2: {K_i} is a non-empty family of subfields of E",
    "¬Q: The intersection of {K_i} is not an algebraically closed subfield of E"
]

N_HYP = 2
NEG_Q_INDEX = 2