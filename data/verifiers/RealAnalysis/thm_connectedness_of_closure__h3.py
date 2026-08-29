import sympy
import sympy.combinatorics
import sympy.matrices
import itertools
import math
import functools

# Top-level setup
# (No specific named objects needed for finite topological spaces, 
# but we provide standard symbols just in case)
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If A is a connected subset of a topological space X, then B is a connected subset of X."
    (The true theorem requires A <= B <= closure(A)).
    """
    try:
        if isinstance(witness, dict):
            X = witness.get('X', [])
            T = witness.get('T', [])
            A = witness.get('A', [])
            B = witness.get('B', [])
        else:
            X, T, A, B = witness
    except Exception:
        return [False, False, False]

    # H_1: X is a topological space (with topology T)
    h1_ok = False
    try:
        X_set = frozenset(X)
        T_sets = set(frozenset(s) for s in T)
        
        is_top = True
        if frozenset() not in T_sets or X_set not in T_sets:
            is_top = False
        else:
            for u in T_sets:
                if not u.issubset(X_set):
                    is_top = False
                    break
                for v in T_sets:
                    if u.intersection(v) not in T_sets:
                        is_top = False
                        break
                    if u.union(v) not in T_sets:
                        is_top = False
                        break
                if not is_top:
                    break
        h1_ok = is_top
    except Exception:
        h1_ok = False

    # H_2: A is a connected subset of X
    h2_ok = False
    try:
        A_set = frozenset(A)
        if A_set.issubset(X_set):
            is_conn = True
            if A_set:
                for u in T_sets:
                    for v in T_sets:
                        if A_set.issubset(u.union(v)):
                            if not u.intersection(v).intersection(A_set):
                                if u.intersection(A_set) and v.intersection(A_set):
                                    is_conn = False
                                    break
                    if not is_conn:
                        break
            h2_ok = is_conn
    except Exception:
        h2_ok = False

    # ¬Q: B is not a connected subset of X
    neg_q_ok = False
    try:
        B_set = frozenset(B)
        if not B_set.issubset(X_set):
            neg_q_ok = True
        else:
            is_conn = True
            if B_set:
                for u in T_sets:
                    for v in T_sets:
                        if B_set.issubset(u.union(v)):
                            if not u.intersection(v).intersection(B_set):
                                if u.intersection(B_set) and v.intersection(B_set):
                                    is_conn = False
                                    break
                    if not is_conn:
                        break
            neg_q_ok = not is_conn
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: A is a connected subset of X",
    "¬Q: B is not a connected subset of X"
]

N_HYP = 2
NEG_Q_INDEX = 2