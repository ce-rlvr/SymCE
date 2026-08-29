import sympy
import math
import itertools
import functools
import z3

x = sympy.Symbol('x', real=True, nonnegative=True)

def conditions(witness):
    """
    Checks if the given witness (a sympy expression in terms of x) is a valid 
    counterexample to the false Fixed Point Theorem for Sublinear Continuous Functions.
    """
    
    def check_h1():
        """
        H_1: f: [0, oo) -> [0, oo) is a continuous function.
        We check non-negativity on [0, oo) and absence of singularities.
        """
        try:
            f = witness
            # Check non-negativity at several sample points
            for val in [0, 0.1, 0.5, 1, 2, 5, 10, 100, 1000]:
                if float(f.subs(x, val)) < 0:
                    return False
            
            # Check for singularities in [0, oo)
            try:
                sings = sympy.singularities(f, x)
                for s in sings:
                    if s.is_real and s >= 0:
                        return False
            except Exception:
                pass
                
            # Check behavior around roots to ensure it doesn't dip below 0
            try:
                roots = sympy.solve(f, x)
                if isinstance(roots, list):
                    for r in roots:
                        if r.is_real and r >= 0:
                            if float(f.subs(x, r + 0.01)) < 0:
                                return False
                            if r - 0.01 >= 0 and float(f.subs(x, r - 0.01)) < 0:
                                return False
            except Exception:
                pass
                
            return True
        except Exception:
            return False

    def check_h2():
        """
        H_2: limsup_{x -> oo} f(x)/x < 1
        """
        try:
            f = witness
            L = sympy.limit(f / x, x, sympy.oo)
            return bool(L < 1)
        except Exception:
            return False

    def check_neg_q():
        """
        ¬Q: There is NO c in (0, oo) such that f(c) = c.
        (The conclusion fails at the witness).
        """
        try:
            f = witness
            # If f(x) is identically x, then every c > 0 is a fixed point.
            if sympy.simplify(f - x) == 0:
                return False
                
            # Solve f(x) = x
            sols = sympy.solve(f - x, x)
            if isinstance(sols, list):
                for s in sols:
                    if s.is_real and s > 0:
                        return False
            return True
        except Exception:
            return False

    return [check_h1(), check_h2(), check_neg_q()]

CONDITION_LABELS = [
    "H_1: f: [0, oo) -> [0, oo) is continuous",
    "H_2: limsup_{x -> oo} f(x)/x < 1",
    "¬Q: There is no c in (0, oo) such that f(c) = c"
]

N_HYP = 2
NEG_Q_INDEX = 2