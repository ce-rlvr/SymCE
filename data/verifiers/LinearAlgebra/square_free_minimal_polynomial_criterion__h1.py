import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x
from sympy import minpoly, factor_list

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "T is diagonalizable if and only if its minimal polynomial over F splits into a product of distinct linear factors."
    """
    # H_1: T is a linear operator on V
    try:
        # A linear operator can be represented by a square matrix
        if hasattr(witness, 'shape') and len(witness.shape) == 2 and witness.shape[0] == witness.shape[1]:
            h1 = True
        elif hasattr(witness, 'is_diagonalizable'):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: The biconditional is false
    try:
        # Check if T is diagonalizable (over the algebraic closure, as is standard in sympy)
        if callable(getattr(witness, 'is_diagonalizable', None)):
            is_diag = witness.is_diagonalizable()
        elif hasattr(witness, 'is_diagonalizable'):
            is_diag = bool(witness.is_diagonalizable)
        else:
            is_diag = False
            
        # Check if the minimal polynomial over F splits into distinct linear factors
        splits_distinct = False
        if callable(getattr(witness, 'minpoly', None)):
            try:
                mp = witness.minpoly(x)
            except Exception:
                mp = witness.minpoly()
        else:
            mp = minpoly(witness, x)
            
        if mp is not None:
            # factor_list factors the polynomial over the domain of its coefficients (field F)
            factors = factor_list(mp)
            splits_distinct = True
            for f, mult in factors[1]:
                if mult > 1:
                    splits_distinct = False
                    break
                if f.as_poly(x).degree() > 1:
                    splits_distinct = False
                    break
        else:
            splits_distinct = False
            
        # The conjecture claims is_diag <==> splits_distinct.
        # The negated conclusion is True if this biconditional fails.
        neg_q = (bool(is_diag) != bool(splits_distinct))
        
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "¬Q: The biconditional 'T is diagonalizable iff its minimal polynomial splits into distinct linear factors' fails"
]

N_HYP = 1
NEG_Q_INDEX = 1