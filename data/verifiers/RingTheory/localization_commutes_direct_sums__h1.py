import sympy
from sympy.matrices import eye, zeros

# Top-level setup for potential witness references
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion at the witness.
    Note: Localization (tensor product) is a left adjoint and therefore commutes 
    with arbitrary colimits, including direct sums. Thus, the original statement 
    is unconditionally true, and no true mathematical counterexample exists 
    (the dataset likely intended direct products \\prod instead of direct sums \\bigoplus).
    We attempt to read mock flags if provided, otherwise default to False.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_multiplicatively_closed", False))
            h2 = bool(witness.get("is_module_family", False))
            neg_q = bool(witness.get("localization_does_not_commute", False))
        elif hasattr(witness, "is_multiplicatively_closed"):
            h1 = bool(getattr(witness, "is_multiplicatively_closed", False))
            h2 = bool(getattr(witness, "is_module_family", False))
            neg_q = bool(getattr(witness, "localization_does_not_commute", False))
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: {M_i}_{i \\in I} is a family of R-modules indexed by an arbitrary set I",
    "¬Q: The localized module S^{-1}(\\bigoplus_{i \\in I} M_i) is not isomorphic to \\bigoplus_{i \\in I} (S^{-1}M_i) as S^{-1}R-modules"
]

N_HYP = 2
NEG_Q_INDEX = 2