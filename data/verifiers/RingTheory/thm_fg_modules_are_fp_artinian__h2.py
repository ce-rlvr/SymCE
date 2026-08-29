import sympy

class MockRing:
    def __init__(self, name, is_artinian):
        self.name = name
        self.is_artinian = is_artinian
        
    def __str__(self):
        return self.name

class MockModule:
    def __init__(self, name, ring, is_finitely_generated, is_finitely_presented):
        self.name = name
        self.ring = ring
        self.is_finitely_generated = is_finitely_generated
        self.is_finitely_presented = is_finitely_presented
        
    def __str__(self):
        return self.name

# Top-level setup: named object bindings for the witness expression
Z = MockRing("Z", is_artinian=False)
Q = MockRing("Q", is_artinian=True)
R = MockRing("R", is_artinian=True)
C = MockRing("C", is_artinian=True)

Q_mod_Q = MockModule("Q_mod_Q", Q, is_finitely_generated=True, is_finitely_presented=True)
Q_infty = MockModule("Q_infty", Q, is_finitely_generated=False, is_finitely_presented=False)
Z_mod_Z = MockModule("Z_mod_Z", Z, is_finitely_generated=True, is_finitely_presented=True)
Z_infty = MockModule("Z_infty", Z, is_finitely_generated=False, is_finitely_presented=False)

def conditions(witness) -> list[bool]:
    # H_1: R is a right Artinian ring
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R_obj = witness[0]
        else:
            R_obj = witness.ring
            
        if hasattr(R_obj, 'is_artinian'):
            h1 = bool(R_obj.is_artinian)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: M is not a finitely presented R-module
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            M_obj = witness[1]
        else:
            M_obj = witness
            
        if hasattr(M_obj, 'is_finitely_presented'):
            neg_q = not bool(M_obj.is_finitely_presented)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: M is not a finitely presented R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1