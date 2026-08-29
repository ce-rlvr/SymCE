import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a PID, then any module M is the direct sum of its p-primary components."
    (The dropped hypothesis is that M is a torsion module).
    
    Expected witness formats:
      - A string like "Z" or "Q" representing the module over Z.
      - A list of invariant factors for a finitely generated Z-module, e.g., [0] for Z, [2, 0] for Z/2Z + Z.
      - A tuple (ring_str, inv_factors), e.g., ("ZZ", [0]).
      - A dict {'R': 'ZZ', 'M_inv_factors': [0]}.
    """
    try:
        # Handle string shortcuts for common counterexamples
        if isinstance(witness, str):
            if witness in ["Q", "QQ", "QQ_over_ZZ", "Z", "ZZ"]:
                return [True, True]
            return [False, False]
            
        # Parse structured witness
        if isinstance(witness, dict):
            ring_str = witness.get("R", "ZZ")
            inv_factors = witness.get("M_inv_factors", [])
        elif isinstance(witness, tuple) and len(witness) == 2:
            ring_str, inv_factors = witness
        elif isinstance(witness, list):
            ring_str = "ZZ"
            inv_factors = witness
        else:
            return [False, False]
            
        if isinstance(inv_factors, (int, str)):
            inv_factors = [inv_factors]
            
        # H_1: R is a principal ideal domain
        pids = ["ZZ", "QQ", "RR", "CC", "QQ[x]", "RR[x]", "CC[x]", "F2[x]", "Fp[x]", "ZZ[i]"]
        h1_ok = ring_str in pids
        
        # ¬Q: M is NOT the direct sum of its p-primary components.
        # For a finitely generated module over a PID, M is the direct sum of its p-primary 
        # components if and only if M is a torsion module.
        # M is a torsion module iff it has no free part (i.e., 0 is not an invariant factor).
        # Thus, the conclusion fails (¬Q is True) iff 0 is among the invariant factors.
        neg_q_ok = (0 in inv_factors) or ("0" in inv_factors) or (sympy.S(0) in inv_factors)
        
        return [bool(h1_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: M is not the direct sum of its p-primary components"
]

N_HYP = 1
NEG_Q_INDEX = 1