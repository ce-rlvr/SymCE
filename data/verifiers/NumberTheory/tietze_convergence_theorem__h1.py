import sympy
import math
import itertools
import functools

n = sympy.Symbol('n')

def evaluate(expr, n_val):
    if callable(expr):
        val = expr(n_val)
    elif hasattr(expr, 'subs'):
        val = expr.subs(n, n_val)
    else:
        val = expr
        
    if hasattr(val, 'evalf'):
        val = complex(val.evalf())
    else:
        val = complex(val)
    return val

def conditions(witness):
    try:
        a, b = witness
    except Exception:
        return [False, False]
        
    H1 = True
    for i in range(1, 101):
        try:
            an = evaluate(a, i)
            bn = evaluate(b, i)
            if abs(bn) < abs(an) + 1 - 1e-9:
                H1 = False
                break
        except Exception:
            H1 = False
            break
            
    converges = True
    # A generalized continued fraction is strictly defined such that a_n != 0.
    # If a_n == 0, it terminates and is not considered a valid infinite continued fraction.
    for i in range(1, 101):
        try:
            an = evaluate(a, i)
            if abs(an) < 1e-9:
                converges = False
                break
        except Exception:
            pass
            
    if converges:
        A_prev, A_curr = 1.0+0j, 0.0+0j
        B_prev, B_curr = 0.0+0j, 1.0+0j
        approximants = []
        for i in range(1, 101):
            try:
                an = evaluate(a, i)
                bn = evaluate(b, i)
                A_next = bn * A_curr + an * A_prev
                B_next = bn * B_curr + an * B_prev
                
                # Normalize to prevent float overflow
                scale = max(abs(A_next), abs(B_next))
                if scale > 1e100:
                    A_next /= scale
                    B_next /= scale
                    A_curr /= scale
                    B_curr /= scale
                    
                A_prev, A_curr = A_curr, A_next
                B_prev, B_curr = B_curr, B_next
                
                if abs(B_curr) > 1e-12:
                    approximants.append(A_curr / B_curr)
                else:
                    converges = False
                    break
            except Exception:
                converges = False
                break
                
        if converges and len(approximants) > 10:
            # Check Cauchy condition for the last few approximants
            diffs = [abs(approximants[i] - approximants[i-1]) for i in range(len(approximants)-10, len(approximants))]
            if max(diffs) > 1e-5:
                converges = False
                
    neg_Q = not converges
    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: |b_n| >= |a_n| + 1 for all n >= 1",
    "¬Q: The generalized continued fraction does not converge"
]

N_HYP = 1
NEG_Q_INDEX = 1