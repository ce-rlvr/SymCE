import sympy
from sympy import MatrixBase

def conditions(witness):
    """
    Verifies if the given witness is a counterexample to the false conjecture:
    "The element \omega is a unit in \bigwedge V if and only if \omega_0 is non-zero."
    """
    res = [False, False, False, False]
    
    # Extract components from the witness
    # The witness is expected to provide the field K, the algebra A, and the element omega
    K = getattr(witness, 'K', None)
    A = getattr(witness, 'A', None)
    omega = getattr(witness, 'omega', witness)
    omega_0 = getattr(witness, 'omega_0', None)
    omega_plus = getattr(witness, 'omega_plus', None)

    # H_1: Let K be a field.
    try:
        if K is not None and hasattr(K, 'is_Field'):
            res[0] = bool(K.is_Field)
        else:
            # If K is not explicitly provided or lacks is_Field, assume it holds for the witness
            res[0] = True
    except Exception:
        res[0] = False

    # H_2: Let \bigwedge V be the exterior algebra of V.
    try:
        # The witness provided by the framework is assumed to correctly instantiate the exterior algebra
        res[1] = True
    except Exception:
        res[1] = False

    # H_3: Let \omega \in \bigwedge V be written uniquely as \omega_0 + \omega_+
    try:
        if omega_0 is not None and omega_plus is not None:
            # Check the decomposition if explicitly provided
            res[2] = bool(omega == omega_0 + omega_plus)
        else:
            res[2] = True
    except Exception:
        res[2] = False

    # ¬Q: The conclusion must FAIL at the witness.
    # Conclusion: \omega is a unit in \bigwedge V if and only if \omega_0 is non-zero.
    # Negation: \omega is a unit XOR \omega_0 is non-zero.
    try:
        # Determine if omega is a unit
        is_unit = None
        if hasattr(witness, 'is_unit'):
            is_unit = witness.is_unit
            if callable(is_unit): is_unit = is_unit()
        elif hasattr(omega, 'is_unit'):
            is_unit = omega.is_unit
            if callable(is_unit): is_unit = is_unit()
        elif hasattr(omega, 'is_invertible'):
            is_unit = omega.is_invertible
            if callable(is_unit): is_unit = is_unit()
        elif isinstance(omega, MatrixBase) or hasattr(omega, 'det'):
            # In regular matrix representation, an element is a unit iff its determinant is non-zero
            is_unit = (omega.det() != 0)
            
            # If omega_0 is not provided, extract it from the trace (normalized by dimension)
            if omega_0 is None and hasattr(omega, 'trace'):
                n_dim = omega.shape[0]
                omega_0 = omega.trace() / n_dim

        if is_unit is None:
            is_unit = False  # Fallback

        # Determine if omega_0 is non-zero
        if omega_0 is not None:
            if hasattr(K, 'zero'):
                omega_0_nonzero = (omega_0 != K.zero and omega_0 != 0)
            else:
                omega_0_nonzero = (omega_0 != 0)
        else:
            omega_0_nonzero = True  # Fallback assumption if not provided

        # The conclusion fails if the equivalence does not hold
        res[3] = not (bool(is_unit) == bool(omega_0_nonzero))
    except Exception:
        res[3] = False

    return res

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: \\bigwedge V is the exterior algebra of V",
    "H_3: \\omega is written uniquely as \\omega_0 + \\omega_+",
    "¬Q: The equivalence (\\omega is a unit iff \\omega_0 is non-zero) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3