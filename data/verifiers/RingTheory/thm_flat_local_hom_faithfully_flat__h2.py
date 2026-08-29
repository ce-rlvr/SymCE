import sympy

class CommutativeRing:
    def __init__(self, name, is_local):
        self.name = name
        self.is_local = is_local
        
    def __str__(self):
        return self.name

class RingHomomorphism:
    def __init__(self, domain, codomain, is_flat, is_faithfully_flat):
        self.domain = domain
        self.codomain = codomain
        self.is_flat = is_flat
        self.is_faithfully_flat = is_faithfully_flat
        
    def __str__(self):
        return f"{self.domain} -> {self.codomain}"

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy does not natively compute flatness or faithfully flatness over abstract rings,
# we provide standard counterexamples and related objects as mock representations.

Z_p = CommutativeRing("Z_{(p)}", is_local=True)
Q = CommutativeRing("Q", is_local=True)
Z = CommutativeRing("Z", is_local=False)
k_x_x = CommutativeRing("k[x]_{(x)}", is_local=True)
k_x_inv = CommutativeRing("k(x)", is_local=True)

# Standard homomorphisms
inclusion_Zp_Q = RingHomomorphism(Z_p, Q, is_flat=True, is_faithfully_flat=False)
identity_Q = RingHomomorphism(Q, Q, is_flat=True, is_faithfully_flat=True)
inclusion_Z_Q = RingHomomorphism(Z, Q, is_flat=True, is_faithfully_flat=False)
inclusion_kxx_kxinv = RingHomomorphism(k_x_x, k_x_inv, is_flat=True, is_faithfully_flat=False)

def conditions(witness) -> list[bool]:
    """
    Given a witness (a RingHomomorphism object), checks if it satisfies the remaining 
    hypotheses and fails the conclusion of the conjecture.
    """
    # H_1: R and S are local rings
    try:
        h1_ok = bool(witness.domain.is_local and witness.codomain.is_local)
    except Exception:
        h1_ok = False

    # H_2: S is a flat R-module via f
    try:
        h2_ok = bool(witness.is_flat)
    except Exception:
        h2_ok = False

    # ¬Q: S is NOT a faithfully flat R-module
    try:
        neg_q_ok = not bool(witness.is_faithfully_flat)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are local rings",
    "H_2: S is a flat R-module via f",
    "¬Q: S is not a faithfully flat R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2