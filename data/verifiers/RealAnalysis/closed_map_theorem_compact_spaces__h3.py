import sympy
from sympy import S, Symbol, solveset, Piecewise, Interval, FiniteSet, Union

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: (X, d_X) is a compact metric space",
    "H_2: (Y, d_Y) is a metric space",
    "¬Q: f is not a closed mapping (there exists closed C in X where f(C) is not closed in Y)"
]

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary providing:
      - 'X': a SymPy set representing the compact metric space (subset of Reals)
      - 'Y': a SymPy set representing the metric space (subset of Reals)
      - 'f_expr': a SymPy expression in terms of `x` representing the mapping f: X -> Y
      - 'C': a SymPy set representing a closed subset of X
      - 'y_limit': a SymPy number representing a limit point of f(C) in Y that is NOT in f(C)
      - 'x_seq_expr': a SymPy expression in terms of `n` representing a sequence in C 
                      such that f(x_seq_expr) converges to y_limit
    """
    X = witness.get('X', S.EmptySet)
    Y = witness.get('Y', S.EmptySet)
    f_expr = witness.get('f_expr', x)
    C = witness.get('C', S.EmptySet)
    y_limit = witness.get('y_limit', S.Zero)
    x_seq_expr = witness.get('x_seq_expr', S.One/n)
    
    def is_compact(S_set):
        if S_set == S.EmptySet:
            return True
        if isinstance(S_set, FiniteSet):
            return True
        if isinstance(S_set, Interval):
            return (not S_set.left_open) and (not S_set.right_open) and \
                   (S_set.start.is_real == True) and (S_set.end.is_real == True)
        if isinstance(S_set, Union):
            return all(is_compact(arg) for arg in S_set.args)
        return False

    # H_1: X is a compact metric space
    try:
        h1 = bool(is_compact(X))
    except Exception:
        h1 = False

    # H_2: Y is a metric space (any subset of Reals is a valid metric space here)
    try:
        h2 = bool(Y.is_subset(S.Reals) == True)
    except Exception:
        h2 = False

    # ¬Q: f is not a closed mapping
    try:
        neg_q = False
        # C must be closed in X (since X is compact, C is closed iff C is compact)
        if is_compact(C) and (C.is_subset(X) == True):
            # y_limit must be in Y
            if Y.contains(y_limit) == True:
                # y_limit must NOT be in f(C)
                sols = solveset(f_expr - y_limit, x, domain=S.Reals)
                if sols.intersect(C) == S.EmptySet:
                    # Verify x_seq_expr is a valid sequence in C
                    seq_valid = True
                    for i in [10, 20, 50, 100]:
                        x_val = x_seq_expr.subs(n, i)
                        if C.contains(x_val) != True:
                            seq_valid = False
                            break
                    
                    if seq_valid:
                        # Verify f(x_seq_expr) converges to y_limit
                        try:
                            lim = sympy.limit(f_expr.subs(x, x_seq_expr), n, sympy.oo)
                            if lim == y_limit:
                                neg_q = True
                        except Exception:
                            pass
                        
                        # Fallback to numerical convergence check if symbolic limit fails
                        if not neg_q:
                            distances = []
                            for i in [10, 100, 1000, 10000, 100000, 1000000]:
                                x_val = x_seq_expr.subs(n, i)
                                f_val = f_expr.subs(x, x_val)
                                dist = abs(f_val - y_limit).evalf()
                                distances.append(dist)
                            
                            is_decreasing = True
                            for j in range(len(distances) - 1):
                                if distances[j+1] >= distances[j]:
                                    is_decreasing = False
                                    break
                            
                            if is_decreasing and distances[-1] <= 1e-5:
                                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, bool(neg_q)]