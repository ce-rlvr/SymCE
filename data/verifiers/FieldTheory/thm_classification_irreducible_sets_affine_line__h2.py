import sympy
from sympy.abc import x, y, z

# Top-level setup
C = sympy.S.Complexes

def check_alg_closed(K):
    if K == sympy.S.Complexes:
        return True
    if isinstance(K, str):
        k_upper = K.upper()
        if 'ALGEBRAICALLY CLOSED' in k_upper or 'ALGEBRAIC CLOSURE' in k_upper:
            return True
        if k_upper in ['C', 'COMPLEXES', 'C_BAR', 'K', 'CC', 'Q_BAR']:
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            K = witness.get('K', None)
            X = witness.get('X', None)
        elif isinstance(witness, tuple) and len(witness) == 2:
            K, X = witness
        else:
            K = None
            X = witness

        try:
            if K is None:
                h1 = False
            else:
                h1 = check_alg_closed(K)
        except Exception:
            h1 = False

        try:
            if isinstance(X, str):
                is_single = False
                is_entire = X.upper() in ['A1', 'A^1', 'AFFINE_LINE', 'AFFINE LINE', 'ENTIRE AFFINE LINE', 'A1(K)', 'A^1(K)']
            elif isinstance(X, (int, float, complex)):
                is_single = True
                is_entire = False
            elif isinstance(X, sympy.Expr):
                if X == 0:
                    is_single = False
                    is_entire = True
                elif not X.free_symbols:
                    is_single = False
                    is_entire = False
                else:
                    roots = sympy.solve(X)
                    if isinstance(roots, dict):
                        is_single = True
                    else:
                        is_single = len(roots) == 1
                    is_entire = False
            elif isinstance(X, sympy.Set):
                if isinstance(X, sympy.FiniteSet):
                    is_single = len(X) == 1
                    is_entire = False
                else:
                    is_single = False
                    is_entire = False
            elif isinstance(X, (set, list, tuple)):
                if len(X) > 0 and all(isinstance(el, sympy.Expr) and el.free_symbols for el in X):
                    roots = sympy.solve(X)
                    if isinstance(roots, dict):
                        is_single = True
                    else:
                        is_single = len(roots) == 1
                    is_entire = all(el == 0 for el in X)
                else:
                    is_single = len(X) == 1
                    is_entire = False
            else:
                is_single = False
                is_entire = False
                
            neg_q = not (is_single or is_entire)
        except Exception:
            neg_q = False

        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: X is neither a single point nor the entire affine line"
]

N_HYP = 1
NEG_Q_INDEX = 1