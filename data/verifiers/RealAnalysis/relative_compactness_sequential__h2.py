import sympy
from sympy import Set, S, Interval, FiniteSet, Union, Intersection
import math
import itertools
import functools

# Top-level setup
R = S.Reals
N = S.Naturals
Z = S.Integers
Q = S.Rationals

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False

    # 1. Dictionary mock
    if isinstance(witness, dict):
        try:
            if 'is_metric_space' in witness:
                h1 = bool(witness['is_metric_space'])
            if 'seq_converges_in_X' in witness:
                h2 = bool(witness['seq_converges_in_X'])
            if 'closure_is_compact' in witness:
                neg_q = not bool(witness['closure_is_compact'])
            if 'is_metric_space' in witness or 'seq_converges_in_X' in witness or 'closure_is_compact' in witness:
                return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. Object mock
    try:
        is_mock = False
        if hasattr(witness, 'is_metric_space'):
            val = witness.is_metric_space() if callable(witness.is_metric_space) else witness.is_metric_space
            h1 = bool(val)
            is_mock = True
        if hasattr(witness, 'seq_converges_in_X'):
            val = witness.seq_converges_in_X() if callable(witness.seq_converges_in_X) else witness.seq_converges_in_X
            h2 = bool(val)
            is_mock = True
        if hasattr(witness, 'closure_is_compact'):
            val = witness.closure_is_compact() if callable(witness.closure_is_compact) else witness.closure_is_compact
            neg_q = not bool(val)
            is_mock = True
        if is_mock:
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. SymPy Sets
    try:
        X = None
        A = None
        
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2 and isinstance(witness[0], Set) and isinstance(witness[1], Set):
                X, A = witness
            elif len(witness) == 3 and isinstance(witness[0], Set) and isinstance(witness[2], Set):
                X, d, A = witness
        elif isinstance(witness, Set):
            X = S.Reals
            A = witness
            
        if X is not None and A is not None:
            # H1: X is a metric space. Subsets of Reals are metric spaces.
            h1 = True
            
            if A.is_subset(X):
                closure_A = A.closure
                # H2: Every sequence in A has a subsequence converging in X
                # For subsets of R, this means A is bounded and its limit points are in X
                h2 = bool(A.is_bounded and closure_A.is_subset(X))
                
                # neg_Q: The closure of A in X is not compact
                # The closure of A in X is closure_A \cap X.
                # It is compact iff it is bounded and closed in R.
                # Since it contains A, its closure in R is closure_A.
                # Thus it is closed in R iff it equals closure_A, i.e., closure_A is a subset of X.
                is_compact = h2
                neg_q = not is_compact
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: Every sequence in A has a subsequence that converges to a limit in X",
    "¬Q: The closure of A in X is not compact"
]

N_HYP = 2
NEG_Q_INDEX = 2