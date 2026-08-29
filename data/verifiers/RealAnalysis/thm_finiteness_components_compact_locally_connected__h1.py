import sympy
from sympy import S, Interval, FiniteSet, Union, ImageSet, Complement, ConditionSet, sin, cos, tan
from sympy.core.relational import StrictGreaterThan, StrictLessThan

# Top-level setup
Z = S.Integers
N = S.Naturals
R = S.Reals

def is_locally_connected(witness):
    """
    Checks if the given SymPy set represents a locally connected topological space
    (assuming the standard subspace topology from the real line).
    """
    if witness in (S.Integers, S.Naturals, S.Naturals0, S.Reals, S.EmptySet):
        return True
    if isinstance(witness, Interval):
        return True
    if isinstance(witness, FiniteSet):
        return True
    if isinstance(witness, Union):
        return all(is_locally_connected(arg) for arg in witness.args)
    if isinstance(witness, ImageSet):
        # Discrete sets are locally connected
        if witness.base_set in (S.Integers, S.Naturals, S.Naturals0):
            return True
    if isinstance(witness, Complement):
        # R \ Z is a union of open intervals, hence locally connected
        if witness.args[0] == S.Reals and witness.args[1] in (S.Integers, S.Naturals, S.Naturals0):
            return True
        # R \ {finite points} is locally connected
        if witness.args[0] == S.Reals and isinstance(witness.args[1], FiniteSet):
            return True
    if isinstance(witness, ConditionSet):
        if witness.base_set == S.Reals:
            # Open conditions generally form open sets in R, which are locally connected
            if isinstance(witness.condition, (StrictGreaterThan, StrictLessThan)):
                return True
    return False

def has_infinitely_many_components(witness):
    """
    Checks if the given SymPy set has infinitely many connected components.
    """
    if witness in (S.Integers, S.Naturals, S.Naturals0):
        return True
    if isinstance(witness, ImageSet):
        if witness.base_set in (S.Integers, S.Naturals, S.Naturals0):
            return True
    if isinstance(witness, Union):
        if any(has_infinitely_many_components(arg) for arg in witness.args):
            return True
    if isinstance(witness, Complement):
        if witness.args[0] == S.Reals and witness.args[1] in (S.Integers, S.Naturals, S.Naturals0):
            return True
    if isinstance(witness, ConditionSet):
        if witness.base_set == S.Reals:
            expr = witness.condition
            # Periodic trigonometric conditions over R typically yield infinitely many components
            if expr.has(sin) or expr.has(cos) or expr.has(tan):
                return True
    return False

def conditions(witness):
    try:
        h1 = bool(is_locally_connected(witness))
    except Exception:
        h1 = False

    try:
        neg_q = bool(has_infinitely_many_components(witness))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: X is a locally connected topological space",
    "¬Q: X has infinitely many connected components"
]

N_HYP = 1
NEG_Q_INDEX = 1