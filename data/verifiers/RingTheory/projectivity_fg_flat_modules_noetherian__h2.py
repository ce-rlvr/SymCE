import sympy

class Ring:
    def __init__(self, name, is_commutative, is_noetherian):
        self.name = name
        self.is_commutative = is_commutative
        self.is_noetherian = is_noetherian
        
    def __str__(self):
        return self.name

class Module:
    def __init__(self, name, ring, is_flat, is_projective):
        self.name = name
        self.ring = ring
        self.is_flat = is_flat
        self.is_projective = is_projective
        
    def __str__(self):
        return f"{self.name} over {self.ring.name}"

# Top-level setup: standard rings and modules for the witness namespace
Z = Ring("Z", is_commutative=True, is_noetherian=True)
Q_ring = Ring("Q", is_commutative=True, is_noetherian=True)
R_ring = Ring("R", is_commutative=True, is_noetherian=True)
C_ring = Ring("C", is_commutative=True, is_noetherian=True)
Poly_inf = Ring("k[x_1, x_2, ...]", is_commutative=True, is_noetherian=False)

Q_as_Z_module = Module("Q", Z, is_flat=True, is_projective=False)
Z_as_Z_module = Module("Z", Z, is_flat=True, is_projective=True)
Z2_as_Z_module = Module("Z/2Z", Z, is_flat=False, is_projective=False)
QZ_as_Z_module = Module("Q/Z", Z, is_flat=False, is_projective=False)

Q_as_Q_module = Module("Q", Q_ring, is_flat=True, is_projective=True)

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    # Try evaluating as custom objects
    try:
        if isinstance(witness, tuple):
            R, M = witness
        else:
            M = witness
            R = M.ring
            
        h1 = bool(R.is_commutative and R.is_noetherian)
        h2 = bool(M.ring == R and M.is_flat)
        neg_q = not bool(M.is_projective)
        return [h1, h2, neg_q]
    except Exception:
        pass
        
    # Fallback for string-based witnesses
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R_str, M_str = witness
            if isinstance(R_str, str) and isinstance(M_str, str):
                h1 = R_str in ["Z", "Q", "R", "C", "Z[x]", "Q[x]"]
                
                if R_str == "Z":
                    if M_str in ["Q", "Z", "Z^2", "Z[x]"]: 
                        h2 = True
                    if M_str in ["Q", "Z/2Z", "Q/Z"]: 
                        neg_q = True
                elif R_str in ["Q", "R", "C"]:
                    h2 = True
                    neg_q = False
                    
                return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: M is a flat R-module",
    "¬Q: M is not a projective R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2