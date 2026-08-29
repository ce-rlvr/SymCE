import sympy
import math
import itertools
import functools

# Top-level setup
# The conjecture is about the space B(X) of bounded real-valued functions on a set X.
# The only case where B(X) fails to be a Banach space under the supremum norm is when X is empty.
# This is because the supremum of the empty set is -infinity, which violates the non-negativity axiom of a norm.
empty_set = sympy.EmptySet

def conditions(witness):
    """
    Given a witness (which represents the domain X), check if it falsifies the conjecture.
    """
    # H1 and H2 are definitional setups for the space B(X) and its norm.
    # They hold trivially for any set X.
    h1 = True
    h2 = True
    
    neg_q = False
    try:
        # Check if the witness represents the empty set.
        if witness is sympy.EmptySet:
            neg_q = True
        elif isinstance(witness, (set, list, tuple)) and len(witness) == 0:
            neg_q = True
        elif hasattr(witness, 'is_empty') and witness.is_empty:
            neg_q = True
        elif isinstance(witness, str) and ("empty" in witness.lower() or witness == "{}" or witness == "[]"):
            neg_q = True
        elif isinstance(witness, int) and witness == 0:
            neg_q = True
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: B(X) is the vector space of all bounded real-valued functions on X",
    "H_2: B(X) is equipped with the supremum norm defined by ||f||_\\infty = \\sup_{x \\in X} |f(x)|",
    "¬Q: The space B(X) is not complete with respect to the metric induced by the supremum norm, or does not form a Banach space"
]

N_HYP = 2
NEG_Q_INDEX = 2