import sympy as sp
from sympy.calculus.util import continuous_domain
import math
import itertools
import functools

# Top-level setup for witness expressions
x = sp.Symbol('x', real=True)
n = sp.Symbol('n', integer=True, positive=True)

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "¬Q: The family of functions {|f| | f in F} is not equicontinuous on X"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        # Parse witness
        if isinstance(witness, dict):
            X = witness.get('X', sp.S.Reals)
            F = witness.get('F', [])
            n_param = witness.get('n', None)
        elif isinstance(witness, (list, tuple)):
            X = sp.S.Reals
            F = list(witness)
            n_param = None
        else:
            X = sp.S.Reals
            F = [witness]
            n_param = None
            
        if not isinstance(F, list):
            F = [F]
            
        # H_1: X is a metric space. Any sympy Set is a metric space under the standard metric.
        h1 = isinstance(X, sp.Set)
        
        # neg_Q: The family {|f| | f in F} is NOT equicontinuous on X.
        # A finite family is equicontinuous iff all members are continuous.
        # We check for discontinuity of |f| to verify it is NOT equicontinuous.
        neg_q = False
        for f in F:
            if isinstance(f, sp.Lambda) and len(f.variables) == 1:
                var = f.variables[0]
                f = f.expr
                
            # Handle Python callables
            if callable(f) and not isinstance(f, sp.Basic):
                test_points = [0.0, 1.0, -1.0, 0.5, -0.5, 2.0, -2.0, 3.1415926535, 2.7182818284]
                eps = 1e-7
                for pt in test_points:
                    try:
                        val = float(abs(f(pt)))
                        val_plus = float(abs(f(pt + eps)))
                        val_minus = float(abs(f(pt - eps)))
                        if abs(val - val_plus) > 1e-2 or abs(val - val_minus) > 1e-2:
                            neg_q = True
                            break
                    except Exception:
                        pass
                if neg_q:
                    break
                continue
                
            if not hasattr(f, 'free_symbols'):
                continue
                
            syms = f.free_symbols
            if n_param is not None and n_param in syms:
                var_candidates = syms - {n_param}
                var = list(var_candidates)[0] if var_candidates else sp.Symbol('x', real=True)
            elif syms:
                var = None
                for s in syms:
                    if s.name == 'x':
                        var = s
                        break
                if var is None:
                    var = list(syms)[0]
            else:
                var = sp.Symbol('x', real=True)
            
            abs_f = sp.Abs(f)
            
            # 1. Symbolic check for discontinuity
            try:
                cont_dom = continuous_domain(abs_f, var, X)
                if not X.is_subset(cont_dom):
                    neg_q = True
                    break
            except Exception:
                pass
                
            # 2. Symbolic check for pointwise limit discontinuity (for sequences)
            if not neg_q and n_param is not None and n_param in syms:
                try:
                    lim_f = sp.limit(abs_f, n_param, sp.oo)
                    cont_dom_lim = continuous_domain(lim_f, var, X)
                    if not X.is_subset(cont_dom_lim):
                        neg_q = True
                        break
                except Exception:
                    pass
                    
            # 3. Numerical fallback for discontinuity
            if not neg_q:
                test_points = [0.0, 1.0, -1.0, 0.5, -0.5, 2.0, -2.0, 3.1415926535, 2.7182818284]
                eps = 1e-7
                for pt in test_points:
                    try:
                        if X.contains(pt) == sp.S.false:
                            continue
                        
                        val = float(abs_f.subs(var, pt).evalf())
                        
                        if X.contains(pt + eps) != sp.S.false:
                            val_plus = float(abs_f.subs(var, pt + eps).evalf())
                            if abs(val - val_plus) > 1e-2:
                                neg_q = True
                                break
                                
                        if X.contains(pt - eps) != sp.S.false:
                            val_minus = float(abs_f.subs(var, pt - eps).evalf())
                            if abs(val - val_minus) > 1e-2:
                                neg_q = True
                                break
                    except Exception:
                        pass
                        
            # 4. Numerical fallback for non-equicontinuity of sequence
            if not neg_q and n_param is not None and n_param in syms:
                test_points = [0.0, 1.0, -1.0, 0.5, -0.5, 2.0, -2.0, 3.1415926535, 2.7182818284]
                eps = 1e-5
                for pt in test_points:
                    try:
                        if X.contains(pt) == sp.S.false:
                            continue
                        
                        expr_n = abs_f.subs(n_param, 100000)
                        val = float(expr_n.subs(var, pt).evalf())
                        
                        if X.contains(pt + eps) != sp.S.false:
                            val_plus = float(expr_n.subs(var, pt + eps).evalf())
                            if abs(val - val_plus) > 0.5:
                                neg_q = True
                                break
                    except Exception:
                        pass
                        
            if neg_q:
                break
                
    except Exception:
        h1 = False
        neg_q = False
        
    return [bool(h1), bool(neg_q)]