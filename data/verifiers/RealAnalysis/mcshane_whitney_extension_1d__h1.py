import sympy
import math
import itertools
import functools

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (S, f, L) where:
      - S is an iterable of real numbers (the domain of f)
      - f is a dictionary or callable mapping elements of S to real numbers
      - L is a real number (the Lipschitz constant)
    """
    try:
        S, f, L = witness
        
        # Normalize f to a callable
        if isinstance(f, dict):
            def eval_f(x):
                return f[x]
        else:
            def eval_f(x):
                return f(x)
                
        # H_1: f is Lipschitz continuous on S with constant L
        # This means for all x, y in S, |f(x) - f(y)| <= L * |x - y|
        h1_ok = True
        for x in S:
            for y in S:
                diff_f = abs(eval_f(x) - eval_f(y))
                diff_x = abs(x - y)
                if not bool(diff_f <= L * diff_x):
                    h1_ok = False
                    break
            if not h1_ok:
                break
                
        # neg_Q: There does NOT exist an extension F: R -> R of f that is L-Lipschitz
        # By the McShane-Whitney extension theorem, an L-Lipschitz extension to R 
        # exists if and only if L >= 0 (since R has multiple points, any L < 0 
        # makes the Lipschitz condition |F(x) - F(y)| <= L * |x - y| impossible for x != y).
        neg_q_ok = bool(L < 0)
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: f: S -> R is Lipschitz continuous with constant L",
    "¬Q: There does not exist an extension F: R -> R of f that is Lipschitz continuous with constant L"
]

N_HYP = 1
NEG_Q_INDEX = 1