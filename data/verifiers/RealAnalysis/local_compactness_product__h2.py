import sympy
from sympy import S, Interval, FiniteSet, Union, Intersection, Set

# Top-level setup: common spaces that might be used in a witness
R = S.Reals
Q = S.Rationals
Z = S.Integers
N = S.Naturals
I = Interval(0, 1)

def is_compact(space):
    """
    Checks if a given SymPy set is a compact metric space (under standard topology).
    """
    if space == S.EmptySet:
        return True
    if isinstance(space, FiniteSet):
        return True
    if isinstance(space, Interval):
        return (not space.left_open) and (not space.right_open) and space.is_bounded
    if isinstance(space, Union):
        return all(is_compact(arg) for arg in space.args)
    if space.__class__.__name__ == 'ProductSet':
        return all(is_compact(arg) for arg in space.args)
    return False

def is_not_locally_compact(space):
    """
    Checks if a given SymPy set is known to NOT be locally compact.
    Returns True only for spaces we are certain are not locally compact.
    """
    if space == S.EmptySet:
        return False
    if space == S.Rationals:
        return True
    if space.__class__.__name__ == 'Complement':
        # Reals \ Rationals (Irrationals)
        if space.args[0] == S.Reals and space.args[1] == S.Rationals:
            return True
    if space.__class__.__name__ == 'ProductSet':
        if any(arg == S.EmptySet for arg in space.args):
            return False
        return any(is_not_locally_compact(arg) for arg in space.args)
    return False

def conditions(witness):
    """
    Given a witness (X, Y), checks if it is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok]
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        X, Y = witness
    except Exception:
        return [False, False]
    
    # H_1: X is a compact metric space
    try:
        h1_ok = bool(is_compact(X))
    except Exception:
        h1_ok = False
        
    # neg_Q: X x Y is NOT locally compact
    try:
        if X == S.EmptySet or Y == S.EmptySet:
            neg_q_ok = False
        else:
            # Since X is compact (hence locally compact), X x Y is not locally compact 
            # if and only if Y is not locally compact.
            neg_q_ok = bool(is_not_locally_compact(Y))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "¬Q: X x Y is not locally compact"
]

N_HYP = 1
NEG_Q_INDEX = 1