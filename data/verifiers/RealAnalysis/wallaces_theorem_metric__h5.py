import math
import sympy

# Top-level setup
# (No specific algebraic objects are required for this topological counterexample)

def is_real_num(x):
    if isinstance(x, (int, float)):
        return True
    if hasattr(x, 'is_real') and x.is_real:
        return True
    return False

def conditions(witness):
    if not isinstance(witness, dict):
        return [False, False, False, False, False]

    # H1: X and Y are metric spaces
    try:
        h1 = witness.get('X') == 'R' and witness.get('Y') == 'R'
    except Exception:
        h1 = False

    # H2: A is a compact subset of X
    try:
        A = witness.get('A')
        h2 = isinstance(A, (list, tuple, set)) and all(is_real_num(x) for x in A)
    except Exception:
        h2 = False

    # H3: B is a compact subset of Y
    try:
        B = witness.get('B')
        h3 = isinstance(B, (list, tuple, set)) and all(is_real_num(x) for x in B)
    except Exception:
        h3 = False

    # H4: W is an open subset of X x Y
    try:
        W = witness.get('W')
        if isinstance(W, list):
            h4 = True
            for rect in W:
                if not (isinstance(rect, (list, tuple)) and len(rect) == 2):
                    h4 = False
                    break
                rx, ry = rect
                if not (isinstance(rx, (list, tuple)) and len(rx) == 2):
                    h4 = False
                    break
                if not (isinstance(ry, (list, tuple)) and len(ry) == 2):
                    h4 = False
                    break
                x1, x2 = rx
                y1, y2 = ry
                if not (is_real_num(x1) and is_real_num(x2) and is_real_num(y1) and is_real_num(y2)):
                    h4 = False
                    break
                if x1 > x2 or y1 > y2:
                    h4 = False
                    break
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: There do NOT exist open U in X, V in Y with A in U, B in V, U x V in W
    # Since A and B are subsets of U and V respectively, U x V in W implies A x B in W.
    # If A x B is NOT a subset of W, then no such U and V can exist.
    try:
        if not h2 or not h3 or not h4:
            neg_q = False
        else:
            def in_W(x, y, W):
                for rect in W:
                    (x1, x2), (y1, y2) = rect
                    if x1 < x < x2 and y1 < y < y2:
                        return True
                return False
            
            subset = True
            for a in A:
                for b in B:
                    if not in_W(a, b, W):
                        subset = False
                        break
                if not subset:
                    break
            
            neg_q = not subset
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: X and Y are metric spaces",
    "H_2: A is a compact subset of X",
    "H_3: B is a compact subset of Y",
    "H_4: W is an open subset of X x Y",
    "¬Q: There do not exist open U in X, V in Y such that A in U, B in V, and U x V in W"
]

N_HYP = 4
NEG_Q_INDEX = 4