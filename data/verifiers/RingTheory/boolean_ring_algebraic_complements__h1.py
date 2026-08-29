import sympy
from sympy import simplify
from sympy.abc import x, y, z

# Top-level setup for Ring Theory
# Witnesses are typically integers, rationals, or symbolic expressions.
# Matrices are omitted here because `1 - x` is not standard sympy syntax for matrices (requires `eye(n) - x`).

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    w = witness
    
    # H_1: Let x be an arbitrary element of R.
    # We verify that the witness supports basic ring operations and can be subtracted from 1.
    try:
        _ = w + w
        _ = w - w
        _ = w * w
        _ = 1 - w
        _ = w * 1
        h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: The conclusion FAILS at the witness.
    # The conclusion is that 1-x satisfies x(1-x) = 0 and x + (1-x) = 1.
    # We check if AT LEAST ONE of these conditions is false.
    try:
        comp = 1 - w
        prod = w * comp
        sum_val = w + comp
        
        # Check if prod == 0
        if hasattr(prod, 'is_zero') and prod.is_zero is not None:
            prod_zero = bool(prod.is_zero)
        else:
            try:
                prod_zero = bool(simplify(prod) == 0)
            except Exception:
                prod_zero = (prod == 0)
                
        # Check if sum_val == 1
        diff = sum_val - 1
        if hasattr(diff, 'is_zero') and diff.is_zero is not None:
            sum_one = bool(diff.is_zero)
        else:
            try:
                sum_one = bool(simplify(diff) == 0)
            except Exception:
                sum_one = (sum_val == 1)
                
        # The conclusion fails if it is NOT the case that both hold
        neg_q = not (prod_zero and sum_one)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of a ring",
    "¬Q: 1-x does not satisfy x(1-x) = 0 and x + (1-x) = 1"
]

N_HYP = 1
NEG_Q_INDEX = 1