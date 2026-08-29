import sympy
from sympy import Symbol, limit, oo, Abs
from sympy.calculus.util import maximum, minimum

# Top-level setup for potential witness objects
# (No specific named groups or matrices are needed for this real analysis theorem)

CONDITION_LABELS = [
    "H_1: D is a subset of the real numbers R",
    "¬Q: The equivalence between uniform continuity and the sequential criterion fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    H1 = False
    neg_Q = False
    
    try:
        if isinstance(witness, dict):
            D = witness.get('D')
            f = witness.get('f')
            try:
                H1 = D.is_subset(sympy.S.Reals)
            except Exception:
                H1 = False
                
            if 'neg_Q' in witness:
                neg_Q = witness['neg_Q']
            elif 'x_n' in witness and 'y_n' in witness:
                x_n = witness['x_n']
                y_n = witness['y_n']
                n = sympy.Symbol('n', integer=True, positive=True)
                x = list(f.free_symbols)[0] if f.free_symbols else sympy.Symbol('x')
                
                lim_diff = limit(Abs(x_n - y_n), n, oo)
                f_x = f.subs(x, x_n)
                f_y = f.subs(x, y_n)
                lim_f_diff = limit(Abs(f_x - f_y), n, oo)
                
                Q_holds = not (lim_diff == sympy.S.Zero and lim_f_diff != sympy.S.Zero)
                
                try:
                    df = f.diff(x)
                    max_val = maximum(df, x, D)
                    min_val = minimum(df, x, D)
                    P_holds = (max_val < oo and min_val > -oo)
                except Exception:
                    P_holds = False
                    
                neg_Q = (P_holds != Q_holds)
                
        elif isinstance(witness, tuple):
            D = witness[0]
            f = witness[1]
            try:
                H1 = D.is_subset(sympy.S.Reals)
            except Exception:
                H1 = False
                
            if len(witness) >= 4:
                x_n = witness[2]
                y_n = witness[3]
                n = sympy.Symbol('n', integer=True, positive=True)
                x = list(f.free_symbols)[0] if f.free_symbols else sympy.Symbol('x')
                
                lim_diff = limit(Abs(x_n - y_n), n, oo)
                f_x = f.subs(x, x_n)
                f_y = f.subs(x, y_n)
                lim_f_diff = limit(Abs(f_x - f_y), n, oo)
                
                Q_holds = not (lim_diff == sympy.S.Zero and lim_f_diff != sympy.S.Zero)
                
                try:
                    df = f.diff(x)
                    max_val = maximum(df, x, D)
                    min_val = minimum(df, x, D)
                    P_holds = (max_val < oo and min_val > -oo)
                except Exception:
                    P_holds = False
                    
                neg_Q = (P_holds != Q_holds)
                
        elif hasattr(witness, 'D') and hasattr(witness, 'f'):
            D = witness.D
            f = witness.f
            try:
                H1 = D.is_subset(sympy.S.Reals)
            except Exception:
                H1 = False
                
            if hasattr(witness, 'neg_Q'):
                if callable(witness.neg_Q):
                    neg_Q = witness.neg_Q()
                else:
                    neg_Q = witness.neg_Q
            elif hasattr(witness, 'x_n') and hasattr(witness, 'y_n'):
                x_n = witness.x_n
                y_n = witness.y_n
                n = sympy.Symbol('n', integer=True, positive=True)
                x = list(f.free_symbols)[0] if f.free_symbols else sympy.Symbol('x')
                
                lim_diff = limit(Abs(x_n - y_n), n, oo)
                f_x = f.subs(x, x_n)
                f_y = f.subs(x, y_n)
                lim_f_diff = limit(Abs(f_x - f_y), n, oo)
                
                Q_holds = not (lim_diff == sympy.S.Zero and lim_f_diff != sympy.S.Zero)
                
                try:
                    df = f.diff(x)
                    max_val = maximum(df, x, D)
                    min_val = minimum(df, x, D)
                    P_holds = (max_val < oo and min_val > -oo)
                except Exception:
                    P_holds = False
                    
                neg_Q = (P_holds != Q_holds)
    except Exception:
        pass

    return [bool(H1), bool(neg_Q)]