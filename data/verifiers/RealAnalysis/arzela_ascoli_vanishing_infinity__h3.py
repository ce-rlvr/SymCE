import sympy as sp
import math
import itertools
import functools

# Top-level setup
x, n = sp.symbols('x n')

def conditions(witness):
    h1 = h2 = h3 = h4 = neg_q = False
    
    try:
        # Normalize witness to dictionary if it's an object
        if not isinstance(witness, dict):
            if hasattr(witness, 'X') and hasattr(witness, 'F'):
                witness = {'X': witness.X, 'F': witness.F}
            elif hasattr(witness, 'domain') and hasattr(witness, 'f'):
                witness = {
                    'domain': witness.domain, 
                    'f': witness.f, 
                    'x': getattr(witness, 'x', x), 
                    'n': getattr(witness, 'n', n)
                }

        if isinstance(witness, dict):
            X = witness.get('X', None)
            F = witness.get('F', None)
            
            if X is not None and F is not None:
                # Case 1: X is a finite discrete space
                if isinstance(X, (list, tuple, set)) and all(isinstance(pt, (int, float)) for pt in X):
                    h1 = h2 = h3 = h4 = True
                    is_bounded = True
                    if callable(F):
                        for pt in X:
                            vals = []
                            for i in range(1, 100):
                                try: vals.append(abs(F(i, pt)))
                                except: pass
                            if vals and max(vals) > 50:
                                is_bounded = False
                    elif isinstance(F, list):
                        for i, pt in enumerate(X):
                            vals = []
                            for f in F:
                                if callable(f):
                                    try: vals.append(abs(f(pt)))
                                    except: pass
                                elif isinstance(f, (list, tuple)) and i < len(f):
                                    vals.append(abs(f[i]))
                            if vals and max(vals) > 50:
                                is_bounded = False
                    neg_q = not is_bounded
                    return [h1, h2, h3, h4, neg_q]
                
                # Case 2: X is a standard infinite space
                elif X in ['R', 'Z', 'R1']:
                    h1 = True
                    if callable(F):
                        if X == 'Z':
                            h2 = h3 = True
                            h4 = True
                            for pt in [100, -100, 1000, -1000]:
                                try:
                                    sup_val = max([abs(F(i, pt)) for i in range(1, 100)] + [0])
                                    if sup_val > 1e-2: h4 = False
                                except: h4 = False
                            
                            is_bounded = True
                            for pt in [0, 1, -1]:
                                try:
                                    vals = [abs(F(i, pt)) for i in range(1, 100)]
                                    if vals and max(vals) > 50: is_bounded = False
                                except: pass
                            neg_q = not is_bounded
                            return [h1, h2, h3, h4, neg_q]
                        else:
                            h2 = True
                            for i in [1, 2, 3]:
                                try:
                                    if abs(F(i, 1000)) > 1e-2 or abs(F(i, -1000)) > 1e-2: h2 = False
                                except: h2 = False
                            
                            h3 = True
                            for i in [1, 10, 200]:
                                try:
                                    if abs(F(i, 0.001) - F(i, 0)) > 0.1: h3 = False
                                except: h3 = False
                                    
                            h4 = True
                            for pt in [1000, -1000]:
                                try:
                                    sup_val = max([abs(F(i, pt)) for i in range(1, 100)] + [0])
                                    if sup_val > 1e-2: h4 = False
                                except: h4 = False
                                    
                            is_bounded = True
                            for pt in [0, 1, -1]:
                                try:
                                    vals = [abs(F(i, pt)) for i in range(1, 100)]
                                    if vals and max(vals) > 50: is_bounded = False
                                except: pass
                            neg_q = not is_bounded
                            return [h1, h2, h3, h4, neg_q]

            # Case 3: Sympy representation
            elif 'domain' in witness and 'f' in witness and 'x' in witness and 'n' in witness:
                domain = witness['domain']
                f_expr = witness['f']
                x_sym = witness['x']
                n_sym = witness['n']
                
                if isinstance(domain, sp.FiniteSet):
                    h1 = h2 = h3 = h4 = True
                    neg_q = False
                    for pt in domain.args:
                        try:
                            lim_f = sp.limit(f_expr.subs(x_sym, pt), n_sym, sp.oo)
                            if getattr(lim_f, 'is_infinite', False) or lim_f in [sp.oo, -sp.oo]:
                                neg_q = True
                                break
                        except: pass
                    return [h1, h2, h3, h4, neg_q]
                
                elif domain == sp.S.Integers:
                    h1 = h3 = True
                    try:
                        h2 = True
                        for n_val in [1, 2, 3]:
                            f_n = f_expr.subs(n_sym, n_val)
                            if sp.limit(f_n, x_sym, sp.oo) != 0 or sp.limit(f_n, x_sym, -sp.oo) != 0:
                                h2 = False
                                break
                    except: h2 = False
                    
                    try:
                        val = f_expr.subs({x_sym: 1000, n_sym: 1000})
                        h4 = (abs(float(val)) < 1e-2)
                    except: h4 = False
                    
                    neg_q = False
                    try:
                        lim_f = sp.limit(f_expr.subs(x_sym, 0), n_sym, sp.oo)
                        if getattr(lim_f, 'is_infinite', False) or lim_f in [sp.oo, -sp.oo]:
                            neg_q = True
                    except: pass
                    return [h1, h2, h3, h4, neg_q]
                
                elif domain == sp.S.Reals:
                    h1 = True
                    try:
                        h2 = True
                        for n_val in [1, 2, 3]:
                            f_n = f_expr.subs(n_sym, n_val)
                            if sp.limit(f_n, x_sym, sp.oo) != 0 or sp.limit(f_n, x_sym, -sp.oo) != 0:
                                h2 = False
                                break
                    except: h2 = False
                    
                    try:
                        df = sp.diff(f_expr, x_sym)
                        if df == 0:
                            h3 = True
                        else:
                            df_at_1_n = df.subs(x_sym, 1/n_sym)
                            lim_df = sp.limit(df_at_1_n, n_sym, sp.oo)
                            if getattr(lim_df, 'is_infinite', False) or lim_df in [sp.oo, -sp.oo]:
                                h3 = False
                            else:
                                lim_df_0 = sp.limit(df.subs(x_sym, 0), n_sym, sp.oo)
                                if getattr(lim_df_0, 'is_infinite', False) or lim_df_0 in [sp.oo, -sp.oo]:
                                    h3 = False
                                else:
                                    h3 = True
                    except: h3 = False
                        
                    try:
                        val = f_expr.subs({x_sym: 1000, n_sym: 1000})
                        h4 = (abs(float(val)) < 1e-2)
                    except: h4 = False
                    
                    try:
                        lim_f = sp.limit(f_expr.subs(x_sym, 0), n_sym, sp.oo)
                        neg_q = getattr(lim_f, 'is_infinite', False) or lim_f in [sp.oo, -sp.oo]
                    except: neg_q = False
                    
                    return [h1, h2, h3, h4, neg_q]

        # Case 4: Bare callable (assume domain is {0, 1})
        if callable(witness):
            h1 = h2 = h3 = h4 = True
            vals = []
            for i in range(1, 100):
                try: vals.append(abs(witness(i, 0)))
                except: pass
                try: vals.append(abs(witness(i, 1)))
                except: pass
            neg_q = len(vals) > 0 and max(vals) > 50
            return [h1, h2, h3, h4, neg_q]
            
    except Exception:
        pass

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: X is a locally compact Hausdorff space",
    "H_2: F is a family of continuous real-valued functions on X that vanish at infinity",
    "H_3: F is equicontinuous on X",
    "H_4: For every epsilon > 0, there exists a compact subset K of X such that |f(x)| < epsilon outside K for all f in F",
    "¬Q: F is not relatively compact in C_0(X)"
]

N_HYP = 4
NEG_Q_INDEX = 4