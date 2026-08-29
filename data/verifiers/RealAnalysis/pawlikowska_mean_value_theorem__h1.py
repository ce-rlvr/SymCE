import sympy
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks the remaining hypotheses and the negated conclusion.
    The witness is expected to be a tuple (f, a, b, n) or a dictionary with these keys,
    where f is a sympy expression in terms of x, a and b are real numbers (a < b),
    and n is a positive integer.
    """
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
            n = witness['n']
        else:
            f, a, b, n = witness
            
        h1 = True
        if float(a) >= float(b) or int(n) < 1:
            h1 = False
        else:
            for k in range(1, int(n) + 1):
                deriv = sympy.diff(f, x, k)
                val_a = deriv.subs(x, a)
                val_b = deriv.subs(x, b)
                diff_val = sympy.simplify(val_a - val_b)
                if diff_val != 0:
                    try:
                        if abs(float(diff_val.evalf())) > 1e-7:
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
            n = witness['n']
        else:
            f, a, b, n = witness
            
        if float(a) >= float(b) or int(n) < 1:
            return [h1, False]
            
        c = sympy.Symbol('c', real=True)
        lhs = f.subs(x, c) - f.subs(x, a)
        rhs = 0
        for k in range(1, int(n) + 1):
            deriv = sympy.diff(f, x, k).subs(x, c)
            term = ((-1)**(k - 1) / sympy.factorial(k)) * (c - a)**k * deriv
            rhs += term
            
        eq = sympy.simplify(lhs - rhs)
        
        if eq == 0:
            neg_q = False
        else:
            has_solution_in_interval = False
            
            # 1. Try exact symbolic solution
            try:
                roots = sympy.solve(eq, c)
                for r in roots:
                    if r.is_real is not False:
                        try:
                            val = float(sympy.re(r.evalf()))
                            if float(a) < val < float(b):
                                if abs(complex(eq.subs(c, val).evalf())) < 1e-4:
                                    has_solution_in_interval = True
                                    break
                        except Exception:
                            pass
            except Exception:
                pass
                
            # 2. Try real_roots if it's a polynomial
            if not has_solution_in_interval:
                try:
                    num = eq.as_numer_denom()[0]
                    if num.is_polynomial(c):
                        rts = sympy.real_roots(num)
                        for r in rts:
                            try:
                                val = float(r.evalf())
                                if float(a) < val < float(b):
                                    if abs(complex(eq.subs(c, val).evalf())) < 1e-4:
                                        has_solution_in_interval = True
                                        break
                            except Exception:
                                pass
                except Exception:
                    pass
                    
            # 3. Fallback to numerical sign-change detection
            if not has_solution_in_interval:
                try:
                    n_points = 1000
                    step = (float(b) - float(a)) / n_points
                    prev_val = None
                    for i in range(1, n_points):
                        pt = float(a) + i * step
                        val = float(eq.subs(c, pt).evalf())
                        if abs(val) < 1e-5:
                            has_solution_in_interval = True
                            break
                        if prev_val is not None and val * prev_val < 0:
                            has_solution_in_interval = True
                            break
                        prev_val = val
                except Exception:
                    pass
                    
            neg_q = not has_solution_in_interval
            
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f^(k)(a) = f^(k)(b) for all k in {1, ..., n}",
    "¬Q: There is no c in (a, b) satisfying the equation"
]

N_HYP = 1
NEG_Q_INDEX = 1