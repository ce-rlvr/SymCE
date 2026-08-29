import sympy
from sympy import Set, Interval, FiniteSet, Union, S, ProductSet

# Top-level setup for potential witness expressions
R = S.Reals
N = S.Naturals
Z = S.Integers
Q = S.Rationals

def is_atsuji(X):
    """
    Helper function to determine if a SymPy Set represents an Atsuji space 
    (a metric space where every continuous function is uniformly continuous).
    For subsets of R, this is closely related to compactness or being uniformly discrete.
    If X is Atsuji, Lipschitz functions are dense in C_b(X).
    """
    if X == S.EmptySet:
        return True
    if isinstance(X, FiniteSet):
        return True
    if X in (S.Integers, S.Naturals, S.Naturals0):
        return True
    if isinstance(X, Union):
        return all(is_atsuji(arg) for arg in X.args)
    if isinstance(X, Interval):
        # An interval is Atsuji iff it is closed and bounded (compact)
        if not X.left_open and not X.right_open:
            if X.start.is_finite and X.end.is_finite:
                return True
        return False
    if isinstance(X, ProductSet):
        return all(is_atsuji(arg) for arg in X.sets)
    if X == S.Reals:
        return False
    if hasattr(X, 'is_compact') and X.is_compact:
        return True
    return False

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # H_1: C(X) is the Banach space of continuous real-valued functions on X with the supremum norm.
        # This is a definitional hypothesis setting the context for the space X.
        if isinstance(witness, Set):
            h1 = True
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], Set):
            h1 = True
        elif isinstance(witness, str):
            h1 = True
        elif hasattr(witness, 'is_subset'):
            h1 = True
    except Exception:
        pass

    try:
        # ¬Q: The set of Lipschitz continuous functions on X is NOT dense in C(X).
        # This occurs when there exist bounded continuous functions on X that cannot be 
        # uniformly approximated by Lipschitz functions (i.e., when X is not an Atsuji space).
        if h1:
            if isinstance(witness, str):
                w_lower = witness.lower()
                if w_lower in ['r', 'reals', '(0, 1)', 'r^n', 'real line', 'r1', 'r2']:
                    neg_q = True
                elif w_lower in ['[0, 1]', 'compact']:
                    neg_q = False
                else:
                    neg_q = True
            else:
                X = witness[0] if isinstance(witness, tuple) else witness
                if isinstance(X, Set) or hasattr(X, 'is_subset'):
                    neg_q = not is_atsuji(X)
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: C(X) is the Banach space of continuous real-valued functions on X with the supremum norm",
    "¬Q: The set of Lipschitz continuous functions on X is not dense in C(X)"
]

N_HYP = 1
NEG_Q_INDEX = 1