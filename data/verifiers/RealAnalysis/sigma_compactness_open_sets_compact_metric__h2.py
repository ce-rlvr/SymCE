import sympy
from sympy import Interval, FiniteSet, Union, Intersection, Complement, S

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)

def is_sigma_compact(U):
    """
    Evaluates whether a given SymPy set U is sigma-compact.
    Returns True if it is (or if it cannot be proven otherwise),
    and False if it is demonstrably not sigma-compact (e.g. the irrationals).
    """
    try:
        if U.is_empty:
            return True
        if isinstance(U, FiniteSet):
            return True
        if U in (S.Rationals, S.Integers, S.Naturals, S.Naturals0):
            return True
        if isinstance(U, Interval):
            return True
        if isinstance(U, Union):
            return all(is_sigma_compact(arg) for arg in U.args)
        
        irrationals = Complement(S.Reals, S.Rationals)
        
        if isinstance(U, Intersection):
            if irrationals in U.args:
                other_args = [arg for arg in U.args if arg != irrationals]
                if len(other_args) == 1 and hasattr(other_args[0], 'measure'):
                    if other_args[0].measure > 0:
                        return False
                        
        if isinstance(U, Complement):
            if U.args[1] == S.Rationals:
                if hasattr(U.args[0], 'measure') and U.args[0].measure > 0:
                    return False
                if U.args[0] == S.Reals:
                    return False
    except Exception:
        pass
    
    # Default to True (meaning not a counterexample) if we can't prove it's not sigma-compact
    return True

def conditions(witness):
    try:
        # The witness can be a tuple (X, U) or just U
        if isinstance(witness, tuple) and len(witness) == 2:
            X, U = witness
        else:
            U = witness
            X = None
            try:
                X = U.closure
            except Exception:
                pass
            
            # Fallback to standard compact spaces if closure is unevaluated or not compact
            if X is None or not (getattr(X, 'is_bounded', False) and getattr(X, 'is_closed', False)):
                if hasattr(U, 'is_subset'):
                    if U.is_subset(Interval(0, 1)):
                        X = Interval(0, 1)
                    elif U.is_subset(Interval(-10, 10)):
                        X = Interval(-10, 10)
                if X is None:
                    X = U
    except Exception:
        return [False, False]

    # H_1: X is a compact metric space (and U is a subset of X)
    try:
        h1_ok = bool(X.is_bounded and X.is_closed and U.is_subset(X))
    except Exception:
        h1_ok = False

    # ¬Q: U is NOT sigma-compact
    try:
        neg_q = not is_sigma_compact(U)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "¬Q: U is not sigma-compact"
]

N_HYP = 1
NEG_Q_INDEX = 1