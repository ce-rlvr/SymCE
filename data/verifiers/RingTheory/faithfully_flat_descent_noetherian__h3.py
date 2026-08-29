import sympy

class Ring:
    def __init__(self, name, commutative=True, noetherian=True):
        self.name = name
        self.commutative = commutative
        self.noetherian = noetherian
        
    def __eq__(self, other):
        if not isinstance(other, Ring):
            return False
        return (self.name == other.name and 
                self.commutative == other.commutative and 
                self.noetherian == other.noetherian)

class RingHom:
    def __init__(self, domain, codomain, faithfully_flat=False):
        self.domain = domain
        self.codomain = codomain
        self.faithfully_flat = faithfully_flat

# Pre-defined rings
Z = Ring("Z", commutative=True, noetherian=True)
Q = Ring("Q", commutative=True, noetherian=True)
Poly_inf_vars = Ring("k[x1, x2, ...]", commutative=True, noetherian=False)

# Pre-defined homomorphisms
id_Z = RingHom(Z, Z, faithfully_flat=True)
id_Q = RingHom(Q, Q, faithfully_flat=True)
id_Poly_inf_vars = RingHom(Poly_inf_vars, Poly_inf_vars, faithfully_flat=True)

def conditions(witness) -> list[bool]:
    try:
        R, S, f = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(R, Ring) and isinstance(S, Ring) and R.commutative and S.commutative
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(f, RingHom) and f.domain == R and f.codomain == S and f.faithfully_flat
    except Exception:
        h2 = False
        
    try:
        neg_q = not R.noetherian
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: f: R -> S is a faithfully flat ring homomorphism",
    "¬Q: R is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2