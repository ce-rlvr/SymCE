import sympy
from sympy import Interval, Union, FiniteSet, Piecewise, Eq, oo

def conditions(witness):
    try:
        # Witness should be a tuple: (domain_X, sequence_f_n, variable_x, variable_n)
        X, f_n, x, n = witness
    except Exception:
        return [False, False, False]
        
    # H1: X is a compact metric space
    try:
        is_subset = X.is_subset(sympy.Reals)
        is_closed = X.boundary.is_subset(X)
        is_bounded = X.inf.is_finite and X.sup.is_finite
        h1 = bool(is_subset and is_closed and is_bounded)
    except Exception:
        h1 = False

    # H2: The sequence {f_n} converges uniformly to a function f on X
    try:
        f = sympy.limit(f_n, n, sympy.oo)
        diff = sympy.simplify(f_n - f)
        
        if diff == 0:
            h2 = True
        elif not diff.has(x):
            lim = sympy.limit(sympy.Abs(diff), n, sympy.oo)
            if not lim.has(sympy.Limit):
                h2 = (lim == 0)
            else:
                h2 = False
        else:
            try:
                from sympy.calculus.util import maximum
                sup = maximum(sympy.Abs(diff), x, X)
                lim_sup = sympy.limit(sup, n, sympy.oo)
                if not lim_sup.has(sympy.Limit):
                    h2 = (lim_sup == 0)
                else:
                    h2 = False
            except Exception:
                # Fallback for Piecewise functions if maximum fails
                if diff.has(sympy.Piecewise):
                    is_unif = True
                    for pw in diff.atoms(sympy.Piecewise):
                        for expr, cond in pw.args:
                            if expr.has(x):
                                try:
                                    from sympy.calculus.util import maximum
                                    sup_expr = maximum(sympy.Abs(expr), x, X)
                                    lim_expr = sympy.limit(sup_expr, n, sympy.oo)
                                    if lim_expr.has(sympy.Limit) or lim_expr != 0:
                                        is_unif = False
                                        break
                                except Exception:
                                    lim_expr = sympy.limit(sympy.Abs(expr), n, sympy.oo)
                                    if lim_expr.has(sympy.Limit) or lim_expr != 0:
                                        is_unif = False
                                        break
                            else:
                                lim_expr = sympy.limit(sympy.Abs(expr), n, sympy.oo)
                                if lim_expr.has(sympy.Limit) or lim_expr != 0:
                                    is_unif = False
                                    break
                        if not is_unif:
                            break
                    h2 = is_unif
                else:
                    h2 = False
    except Exception:
        h2 = False

    # neg_Q: The family of functions {f_n} is NOT equicontinuous on X
    # Since uniform convergence of continuous functions on a compact set implies equicontinuity,
    # equicontinuity fails here if and only if some f_n is discontinuous on X.
    try:
        is_continuous = True
        for n_val in [1, 2]:
            f_val = f_n.subs(n, n_val)
            
            # 1. Check for explicit singularities
            try:
                from sympy.calculus.singularities import singularities
                sings = singularities(f_val, x)
                for p in sings:
                    if p.is_real and p in X:
                        is_continuous = False
                        break
            except Exception:
                pass
                
            if not is_continuous:
                break
                
            # 2. Check using continuous_domain
            try:
                from sympy.calculus.util import continuous_domain
                cont_dom = continuous_domain(f_val, x, sympy.Reals)
                if isinstance(cont_dom, sympy.Complement):
                    pts = cont_dom.args[1]
                    if isinstance(pts, sympy.FiniteSet):
                        for p in pts:
                            if p.is_real and p in X:
                                val = f_val.subs(x, p)
                                
                                left_nhbd = sympy.Interval.Lopen(-sympy.oo, p)
                                int_left = sympy.Intersection(X, left_nhbd)
                                is_limit_left = False
                                if not int_left.is_empty:
                                    try:
                                        is_limit_left = (int_left.sup == p)
                                    except Exception:
                                        pass
                                        
                                right_nhbd = sympy.Interval.Ropen(p, sympy.oo)
                                int_right = sympy.Intersection(X, right_nhbd)
                                is_limit_right = False
                                if not int_right.is_empty:
                                    try:
                                        is_limit_right = (int_right.inf == p)
                                    except Exception:
                                        pass
                                        
                                if is_limit_left:
                                    lim_left = sympy.limit(f_val, x, p, dir='-')
                                    if not lim_left.has(sympy.Limit) and lim_left != val:
                                        is_continuous = False
                                        break
                                if is_limit_right:
                                    lim_right = sympy.limit(f_val, x, p, dir='+')
                                    if not lim_right.has(sympy.Limit) and lim_right != val:
                                        is_continuous = False
                                        break
            except Exception:
                pass
                
            if not is_continuous:
                break
                
            # 3. Check Piecewise boundaries
            if f_val.has(sympy.Piecewise):
                for pw in f_val.atoms(sympy.Piecewise):
                    for expr, cond in pw.args:
                        rels = []
                        if isinstance(cond, sympy.Rel):
                            rels.append(cond)
                        elif isinstance(cond, sympy.Boolean):
                            rels.extend(cond.atoms(sympy.Rel))
                            
                        for rel in rels:
                            try:
                                eq = sympy.Eq(rel.lhs, rel.rhs)
                                pts = sympy.solve(eq, x)
                                for p in pts:
                                    if p.is_real and p in X:
                                        val = f_val.subs(x, p)
                                        
                                        left_nhbd = sympy.Interval.Lopen(-sympy.oo, p)
                                        int_left = sympy.Intersection(X, left_nhbd)
                                        is_limit_left = False
                                        if not int_left.is_empty:
                                            try:
                                                is_limit_left = (int_left.sup == p)
                                            except Exception:
                                                pass
                                                
                                        right_nhbd = sympy.Interval.Ropen(p, sympy.oo)
                                        int_right = sympy.Intersection(X, right_nhbd)
                                        is_limit_right = False
                                        if not int_right.is_empty:
                                            try:
                                                is_limit_right = (int_right.inf == p)
                                            except Exception:
                                                pass
                                                
                                        if is_limit_left:
                                            lim_left = sympy.limit(f_val, x, p, dir='-')
                                            if not lim_left.has(sympy.Limit) and lim_left != val:
                                                is_continuous = False
                                                break
                                        if is_limit_right:
                                            lim_right = sympy.limit(f_val, x, p, dir='+')
                                            if not lim_right.has(sympy.Limit) and lim_right != val:
                                                is_continuous = False
                                                break
                            except Exception:
                                pass
            if not is_continuous:
                break
                
        neg_q = not is_continuous
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: The sequence {f_n} converges uniformly to a function f on X",
    "¬Q: The family of functions {f_n} is not equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2