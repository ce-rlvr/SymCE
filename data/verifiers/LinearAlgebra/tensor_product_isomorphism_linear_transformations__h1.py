import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_dim(obj):
    """Attempt to extract a dimension or shape from an object."""
    if hasattr(obj, 'dimension'):
        return obj.dimension
    if hasattr(obj, 'dim'):
        return obj.dim
    if hasattr(obj, 'shape'):
        try:
            return obj.shape[0] * obj.shape[1]
        except Exception:
            pass
    return obj

def is_infinite(d):
    """Check if the dimension represents an infinite value."""
    d = get_dim(d)
    try:
        if d == sympy.oo or d == float('inf'):
            return True
        if hasattr(d, 'is_infinite') and d.is_infinite:
            return True
        if isinstance(d, str) and ('inf' in d.lower() or 'oo' in d.lower()):
            return True
    except Exception:
        pass
    return False

def is_finite(d):
    """Check if the dimension represents a finite value."""
    d = get_dim(d)
    if is_infinite(d):
        return False
    try:
        if isinstance(d, str) and 'fin' in d.lower():
            return True
        if hasattr(d, 'is_finite') and d.is_finite:
            return True
        val = int(d)
        return val >= 0
    except Exception:
        return False

def conditions(witness):
    """
    Evaluates the remaining hypotheses and the negated conclusion.
    The AI is expected to provide a witness where V is infinite-dimensional 
    and W is finite-dimensional, based on the common misconception that the 
    isomorphism requires BOTH spaces to be finite-dimensional.
    """
    try:
        # Parse the witness to extract dimensions of V and W
        if isinstance(witness, dict):
            dim_V = witness.get('dim_V', witness.get('V', witness.get('dim', sympy.oo)))
            dim_W = witness.get('dim_W', witness.get('W', 1))
        elif hasattr(witness, 'dim_V') and hasattr(witness, 'dim_W'):
            dim_V = witness.dim_V
            dim_W = witness.dim_W
        elif hasattr(witness, 'V') and hasattr(witness, 'W'):
            dim_V = witness.V
            dim_W = witness.W
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                dim_V, dim_W = witness
            elif len(witness) == 1:
                dim_V = witness[0]
                dim_W = 1
            else:
                return [False, False]
        else:
            dim_V = witness
            dim_W = 1
    except Exception:
        return [False, False]

    # H_1: W is a finite-dimensional vector space over the field F
    try:
        h1_ok = is_finite(dim_W)
    except Exception:
        h1_ok = False

    # ¬Q: L(V, W) is not naturally isomorphic to V* \otimes W
    # The conclusion is expected to fail when V is infinite-dimensional.
    try:
        neg_q_ok = is_infinite(dim_V)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    r"H_1: W is a finite-dimensional vector space over the field F",
    r"¬Q: L(V, W) is not naturally isomorphic to V* \otimes W"
]

N_HYP = 1
NEG_Q_INDEX = 1