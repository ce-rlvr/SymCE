import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide the space X, distance function d, subset A, and optionally f.
    """
    if isinstance(witness, dict):
        X = witness.get('X', [])
        d = witness.get('d', {})
        A = witness.get('A', [])
        f = witness.get('f', None)
    elif isinstance(witness, tuple):
        X = witness[0] if len(witness) > 0 else []
        d = witness[1] if len(witness) > 1 else {}
        A = witness[2] if len(witness) > 2 else []
        f = witness[3] if len(witness) > 3 else None
    else:
        X = getattr(witness, 'X', [])
        d = getattr(witness, 'd', {})
        A = getattr(witness, 'A', [])
        f = getattr(witness, 'f', None)

    try:
        X_list = list(X)
        A_list = list(A)
    except Exception:
        return [False, False, False]

    # H_1: Let A be a non-empty subset of X.
    try:
        h1 = len(A_list) > 0 and all(a in X_list for a in A_list)
    except Exception:
        h1 = False

    # If f is not provided, compute it as per H_2
    try:
        if f is None:
            f_dict = {}
            for x in X_list:
                if callable(d):
                    f_dict[x] = min(d(x, a) for a in A_list)
                else:
                    f_dict[x] = min(d[(x, a)] for a in A_list)
            f = f_dict
    except Exception:
        pass

    # H_2: Let f: X -> R be defined by f(x) = inf_{a in A} d(x, a).
    try:
        h2 = True
        for x in X_list:
            if callable(d):
                inf_val = min(d(x, a) for a in A_list)
            else:
                inf_val = min(d[(x, a)] for a in A_list)
            
            if callable(f):
                fx = f(x)
            else:
                fx = f[x]
                
            if abs(float(fx) - float(inf_val)) > 1e-9:
                h2 = False
                break
    except Exception:
        h2 = False

    # ¬Q: The function f is NOT Lipschitz continuous on X with Lipschitz constant 1.
    # This means there exist x, y in X such that |f(x) - f(y)| > d(x, y).
    try:
        neg_q = False
        for x in X_list:
            for y in X_list:
                if callable(f):
                    fx = f(x)
                    fy = f(y)
                else:
                    fx = f[x]
                    fy = f[y]
                
                if callable(d):
                    d_xy = d(x, y)
                else:
                    d_xy = d[(x, y)]
                
                if abs(float(fx) - float(fy)) > float(d_xy) + 1e-9:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a non-empty subset of X",
    "H_2: f(x) = inf_{a in A} d(x, a)",
    "¬Q: f is not Lipschitz continuous on X with Lipschitz constant 1"
]

N_HYP = 2
NEG_Q_INDEX = 2