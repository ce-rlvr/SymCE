import sympy
from sympy import Symbol, Interval, FiniteSet, Union, Intersection, EmptySet, limit, oo
from itertools import combinations

# Top-level setup for the witness namespace
n = Symbol('n', integer=True, positive=True)
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (X, F_n, n) or (X, F_n) or (X, F_callable)
    where X is a compact metric space (SymPy Set) and F_n is a SymPy Set parameterized by n.
    """
    X = None
    F_n = None
    n_sym = None
    
    # Extract X, F_n, and the symbol n from the witness
    if isinstance(witness, tuple):
        if len(witness) == 3:
            X, F_n, n_sym = witness
        elif len(witness) == 2:
            X, F = witness
            if callable(F):
                n_sym = Symbol('n', integer=True, positive=True)
                try:
                    F_n = F(n_sym)
                except Exception:
                    pass
            else:
                F_n = F
                try:
                    free = F_n.free_symbols
                    if len(free) == 1:
                        n_sym = list(free)[0]
                    else:
                        n_sym = n
                except Exception:
                    n_sym = n

    if X is None or F_n is None or n_sym is None:
        return [False, False, False]

    # H_1: (X, d) is a compact metric space and F is a collection of subsets of X
    def is_compact(S):
        if S == EmptySet:
            return True
        if isinstance(S, FiniteSet):
            return True
        if isinstance(S, Interval):
            return not S.left_open and not S.right_open and S.start.is_finite and S.end.is_finite
        if isinstance(S, Union):
            return all(is_compact(arg) for arg in S.args)
        return False

    def is_subset_of_X(F_n, n_sym, X):
        for i in range(1, 11):
            try:
                Fi = F_n.subs(n_sym, i)
                sub = Fi.is_subset(X)
                if sub is False:
                    return False
                if sub is None:
                    # Fallback for intervals if SymPy cannot decide symbolically
                    if isinstance(Fi, Interval) and isinstance(X, Interval):
                        try:
                            if bool(Fi.start < X.start) or bool(Fi.end > X.end):
                                return False
                        except TypeError:
                            pass
            except Exception:
                pass
        return True

    try:
        h1 = is_compact(X) and is_subset_of_X(F_n, n_sym, X)
    except Exception:
        h1 = False

    # H_2: Every finite subcollection of F has a non-empty intersection
    try:
        h2 = True
        sets = [F_n.subs(n_sym, i) for i in range(1, 11)]
        for r in range(1, 4):
            for combo in combinations(sets, r):
                if Intersection(*combo) == EmptySet:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # ¬Q: The intersection of all sets in the collection F is empty
    try:
        neg_q = False
        if F_n == EmptySet:
            neg_q = True
        elif isinstance(F_n, Interval):
            L_n = F_n.start
            U_n = F_n.end
            L = limit(L_n, n_sym, oo)
            U = limit(U_n, n_sym, oo)
            try:
                if bool(L > U):
                    neg_q = True
                elif bool(L < U):
                    neg_q = False
                else:
                    # L == U, the only possible point in the intersection is L
                    neg_q = False
                    for i in range(1, 100):
                        if not F_n.subs(n_sym, i).contains(L):
                            neg_q = True
                            break
            except TypeError:
                neg_q = False
        else:
            # Fallback for non-intervals: assume false unless trivially empty
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (X, d) is a compact metric space",
    "H_2: Every finite subcollection of F has a non-empty intersection",
    "¬Q: The intersection of all sets in the collection F is empty"
]

N_HYP = 2
NEG_Q_INDEX = 2