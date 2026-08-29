import sympy
from sympy import Rational, Integer
import math

# Top-level setup
# We don't need complex algebraic structures for this real analysis conjecture.
# The witness will likely be a set of rational numbers (e.g., {x in Q | x^2 < 2})
# represented as a list, a set, or a custom object.
# We will evaluate the conditions on the witness.

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    Hypotheses:
      - S is non-empty
      - S is bounded above
    Conclusion:
      - S has a supremum in the real numbers.
      
    Wait, if S is a subset of the rational numbers, it DOES have a supremum in the real numbers.
    The only way a non-empty, bounded above set does NOT have a supremum in the real numbers
    is if it's a subset of some other ordered set (like the hyperreals, or rational functions)
    where the supremum doesn't exist in the reals, or if the witness is a set of reals but
    the supremum is infinity (which violates bounded above).
    Actually, if the witness is a set of rational numbers, and the conclusion is "S has a supremum in the rational numbers",
    then the negation is true (e.g., {x in Q | x^2 < 2}).
    Assuming the prompt meant "S has a supremum in the rational numbers" or the witness is a subset of Q.
    We will check if the witness is non-empty, bounded above, and does NOT have a supremum in the reals.
    Wait, if the witness is a subset of Q, it has a supremum in R.
    Let's just evaluate the literal conditions.
    """
    
    # H1: S is non-empty
    try:
        h1_ok = len(witness) > 0 if hasattr(witness, '__len__') else True
        # If it's a custom object representing a set, we assume it's non-empty if it can be instantiated
        # or we can check a specific method.
        if hasattr(witness, 'is_empty'):
            h1_ok = not witness.is_empty()
    except Exception:
        h1_ok = False

    # H2: S is bounded above
    try:
        h2_ok = False
        if hasattr(witness, 'is_bounded_above'):
            h2_ok = witness.is_bounded_above()
        elif hasattr(witness, 'upper_bound'):
            h2_ok = witness.upper_bound() is not None
        elif isinstance(witness, (list, set, tuple)):
            # A finite set of numbers is always bounded above
            h2_ok = all(isinstance(x, (int, float, Rational, Integer, sympy.Expr)) for x in witness)
    except Exception:
        h2_ok = False

    # ¬Q: S does NOT have a supremum in the real numbers
    try:
        neg_q = False
        if hasattr(witness, 'has_real_supremum'):
            neg_q = not witness.has_real_supremum()
        elif hasattr(witness, 'supremum'):
            sup = witness.supremum()
            # If supremum is not in reals (e.g., it's a hyperreal or doesn't exist)
            if sup is None:
                neg_q = True
            else:
                # If it returns a value, we check if it's a real number
                neg_q = not sup.is_real if hasattr(sup, 'is_real') else False
        elif isinstance(witness, (list, set, tuple)):
            # A finite set of real numbers always has a supremum in the real numbers (its maximum)
            neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: S is non-empty",
    "H_2: S is bounded above",
    "¬Q: S does not have a supremum in the real numbers"
]

N_HYP = 2
NEG_Q_INDEX = 2