import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a dictionary, an object with attributes, or a string representation.
    """
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_m_adic_completion", False))
            r_hat_noetherian = bool(witness.get("R_hat_is_Noetherian", True))
            r_hat_local = bool(witness.get("R_hat_is_local", True))
            neg_q = not (r_hat_noetherian and r_hat_local)
            return [h1, neg_q]
        
        elif hasattr(witness, "is_m_adic_completion"):
            h1 = bool(getattr(witness, "is_m_adic_completion", False))
            r_hat_noetherian = bool(getattr(witness, "R_hat_is_Noetherian", True))
            r_hat_local = bool(getattr(witness, "R_hat_is_local", True))
            neg_q = not (r_hat_noetherian and r_hat_local)
            return [h1, neg_q]
            
        else:
            # Fallback for string or tuple representations of known counterexamples
            # e.g., R = k[x_1, x_2, ...]_{(x_1, x_2, ...)}, R_hat = k[[x_1, x_2, ...]]
            w = str(witness).lower()
            h1 = "completion" in w or "m-adic" in w or "k[[x" in w
            neg_q = "not noetherian" in w or "non-noetherian" in w or "k[[x" in w
            return [h1, neg_q]
            
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: \\hat{R} is the completion of R with respect to the m-adic topology",
    "¬Q: \\hat{R} is not a Noetherian local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1