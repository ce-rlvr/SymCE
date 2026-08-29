import sympy
from sympy import symbols

# Top-level setup
# SymPy does not natively support computing depth and Krull dimension for arbitrary 
# non-Noetherian local rings. The witness is expected to be a dictionary or an object 
# exposing the relevant precomputed properties.

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness should provide 'm_is_maximal_ideal', 'depth', and 'krull_dimension'.
    """
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('m_is_maximal_ideal', 
                      witness.get('is_maximal_ideal', 
                      witness.get('is_local', False))))
            depth = witness.get('depth', 0)
            dim = witness.get('krull_dimension', witness.get('dim', float('inf')))
        else:
            h1 = bool(getattr(witness, 'm_is_maximal_ideal', 
                      getattr(witness, 'is_maximal_ideal', 
                      getattr(witness, 'is_local', False))))
            depth = getattr(witness, 'depth', 0)
            dim = getattr(witness, 'krull_dimension', getattr(witness, 'dim', float('inf')))
            
        # The conclusion is that depth <= Krull dimension.
        # The negated conclusion is that depth > Krull dimension.
        neg_q = depth > dim
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: \mathfrak{m} is the maximal ideal of R",
    "¬Q: The depth of R with respect to \mathfrak{m} is strictly greater than the Krull dimension of R"
]

N_HYP = 1
NEG_Q_INDEX = 1