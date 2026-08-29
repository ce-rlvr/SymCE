import sympy
from sympy import Symbol, Expr, diff, limit, oo, lambdify, Set, S, symbols, FiniteSet, sympify
import math
import itertools
import functools

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: A is a non-empty subset of the real numbers",
    "¬Q: f is not uniformly continuous on the real line"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    A = None
    f = None
    
    # Parse witness
    if isinstance(witness, tuple) and len(witness) == 2:
        A, f = witness
    elif isinstance(witness, dict):
        A = witness.get('A')
        f = witness.get('f')
    elif hasattr(witness, 'A') and hasattr(witness, 'f'):
        A = witness.A
        f = witness.f
    else:
        return [False, False]

    # H1: A is a non-empty subset of the real numbers
    h1 = False
    try:
        if isinstance(A, (list, tuple, set)):
            A = FiniteSet(*A)
        if isinstance(A, Set) and not A.is_empty and A.is_subset(S.Reals):
            h1 = True
    except Exception:
        pass

    # neg_Q: f is NOT uniformly continuous on the real line
    neg_q = False
    try:
        if isinstance(f, str):
            f = sympify(f)
            
        if isinstance(f, Expr):
            free = f.free_symbols
            if len(free) == 1:
                sym_x = list(free)[0]
                
                # Check if defined at basic points (if not, it's not uniformly continuous on R)
                try:
                    f_num = lambdify(sym_x, f, 'math')
                    for test_val in [-10, -1, 0, 1, 10]:
                        f_num(test_val)
                except Exception:
                    # Fallback to evalf to verify domain errors
                    for test_val in [-10, -1, 0, 1, 10]:
                        try:
                            val = f.subs(sym_x, test_val).evalf()
                            if not val.is_real:
                                neg_q = True
                                break
                        except Exception:
                            neg_q = True
                            break
                            
                if not neg_q:
                    df = diff(f, sym_x)
                    try:
                        L1 = limit(df, sym_x, oo)
                        if L1 in [oo, -oo]: neg_q = True
                    except Exception: 
                        pass
                    
                    try:
                        L2 = limit(df, sym_x, -oo)
                        if L2 in [oo, -oo]: neg_q = True
                    except Exception: 
                        pass
                    
                if not neg_q:
                    try:
                        f_num = lambdify(sym_x, f, 'math')
                        f_num(10) # Test lambdify works
                        for val in [10, 100, 1000, 10000, 100000]:
                            for offset in [0, 1, 2, 3]:
                                try:
                                    v = val + offset
                                    df_val = (f_num(v + 1e-5) - f_num(v)) / 1e-5
                                    if abs(df_val) > 1000:
                                        neg_q = True
                                        break
                                    df_val_neg = (f_num(-v + 1e-5) - f_num(-v)) / 1e-5
                                    if abs(df_val_neg) > 1000:
                                        neg_q = True
                                        break
                                except Exception:
                                    # Overflow or domain error at large values implies not uniformly continuous
                                    neg_q = True
                                    break
                            if neg_q:
                                break
                    except Exception:
                        # Fallback to evalf if lambdify fails
                        for val in [10, 100, 1000, 10000]:
                            for offset in [0, 1, 2]:
                                try:
                                    v = val + offset
                                    f_v = f.subs(sym_x, v).evalf()
                                    f_v_plus = f.subs(sym_x, v + 1e-4).evalf()
                                    df_val = (f_v_plus - f_v) / 1e-4
                                    if abs(df_val) > 1000:
                                        neg_q = True
                                        break
                                        
                                    f_nv = f.subs(sym_x, -v).evalf()
                                    f_nv_plus = f.subs(sym_x, -v + 1e-4).evalf()
                                    df_val_neg = (f_nv_plus - f_nv) / 1e-4
                                    if abs(df_val_neg) > 1000:
                                        neg_q = True
                                        break
                                except Exception:
                                    neg_q = True
                                    break
                            if neg_q:
                                break
                                
        elif callable(f):
            try:
                for test_val in range(-10, 11):
                    f(test_val)
            except Exception:
                neg_q = True
                
            if not neg_q:
                for val in [10, 100, 1000, 10000, 100000]:
                    for offset in [0, 1, 2, 3]:
                        try:
                            v = val + offset
                            df_val = (f(v + 1e-5) - f(v)) / 1e-5
                            if abs(df_val) > 1000:
                                neg_q = True
                                break
                            df_val_neg = (f(-v + 1e-5) - f(-v)) / 1e-5
                            if abs(df_val_neg) > 1000:
                                neg_q = True
                                break
                        except Exception:
                            neg_q = True
                            break
                    if neg_q:
                        break
    except Exception:
        pass

    return [bool(h1), bool(neg_q)]