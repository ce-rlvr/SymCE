import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    
    Remaining hypothesis:
      H_1: Let V be a finite-dimensional vector space.
      
    Conclusion to falsify:
      Q: The vector space V can be expressed as a direct sum of non-zero T-cyclic invariant subspaces.
      (Fails exactly when V is the zero vector space, i.e., dimension is 0, because there are no non-zero subspaces).
    """
    h1_ok = False
    n = -1
    
    try:
        # Determine if the witness represents a finite-dimensional vector space (or an operator on it)
        # and extract its dimension.
        if isinstance(witness, int):
            if witness >= 0:
                h1_ok = True
                n = witness
        elif hasattr(witness, 'is_square') and witness.is_square:
            h1_ok = True
            n = witness.shape[0]
        elif hasattr(witness, 'dimension'):
            dim = witness.dimension() if callable(witness.dimension) else witness.dimension
            if isinstance(dim, int) and dim >= 0:
                h1_ok = True
                n = dim
        elif isinstance(witness, (tuple, list)):
            for item in witness:
                if hasattr(item, 'is_square') and item.is_square:
                    h1_ok = True
                    n = item.shape[0]
                    break
            if not h1_ok and len(witness) > 0 and isinstance(witness[0], int) and witness[0] >= 0:
                h1_ok = True
                n = witness[0]
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        # The conclusion fails if and only if the vector space has dimension 0.
        # In a 0-dimensional space, there are no non-zero vectors to generate non-zero T-cyclic subspaces.
        if h1_ok and n == 0:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "¬Q: V cannot be expressed as a direct sum of non-zero T-cyclic invariant subspaces"
]

N_HYP = 1
NEG_Q_INDEX = 1