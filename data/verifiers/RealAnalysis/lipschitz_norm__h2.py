import sympy
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for potential witness expressions
R = 'R'

def conditions(witness) -> list[bool]:
    f = None
    is_normed_vs = False
    
    # Extract the function and vector space from the witness
    try:
        if isinstance(witness, dict):
            f = witness.get('f', witness.get('func', None))
            v = witness.get('V', 'R')
            if isinstance(v, str) and v.startswith('R'):
                is_normed_vs = True
            elif v is not None:
                is_normed_vs = True
        else:
            f = witness
            is_normed_vs = True
            
        if f is None:
            h1 = False
        else:
            # Check if f is a valid mathematical object (callable, sympy expr, or constant)
            if callable(f) or hasattr(f, 'free_symbols') or isinstance(f, (int, float)):
                h1 = is_normed_vs
            else:
                h1 = False
    except Exception:
        h1 = False

    neg_q = False
    try:
        if h1:
            # Grid of points to test for Lipschitz continuity violation
            points = [i/2.0 for i in range(-20, 21)] + [30.0, -30.0, 50.0, -50.0, 100.0, -100.0]
            
            if callable(f):
                evaluated = []
                for pt in points:
                    try:
                        val = float(f(pt))
                        evaluated.append((pt, val))
                    except Exception:
                        pass
                
                # Check all pairs for Lipschitz constant > 1
                for i in range(len(evaluated)):
                    for j in range(i+1, len(evaluated)):
                        x_val, fx = evaluated[i]
                        y_val, fy = evaluated[j]
                        if abs(fx - fy) > abs(x_val - y_val) + 1e-7:
                            neg_q = True
                            break
                    if neg_q:
                        break
            else:
                if hasattr(f, 'free_symbols'):
                    free_syms = list(f.free_symbols)
                else:
                    free_syms = []
                    
                if len(free_syms) == 0:
                    # Constant functions have Lipschitz constant 0 <= 1
                    neg_q = False
                else:
                    sym = free_syms[0]
                    evaluated = []
                    for pt in points:
                        # Evaluate along one axis if multi-variable
                        subs_dict = {s: 0.0 for s in free_syms}
                        subs_dict[sym] = pt
                        try:
                            val = float(f.subs(subs_dict))
                            evaluated.append((pt, val))
                        except Exception:
                            pass
                            
                    # Check all pairs for Lipschitz constant > 1
                    for i in range(len(evaluated)):
                        for j in range(i+1, len(evaluated)):
                            x_val, fx = evaluated[i]
                            y_val, fy = evaluated[j]
                            if abs(fx - fy) > abs(x_val - y_val) + 1e-7:
                                neg_q = True
                                break
                        if neg_q:
                            break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (V, ||.||) is a normed vector space",
    "¬Q: The function f is NOT Lipschitz continuous on V with Lipschitz constant 1"
]

N_HYP = 1
NEG_Q_INDEX = 1