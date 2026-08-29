import sympy
import z3
import math
import itertools
import functools

# Top-level setup
x_sym = sympy.Symbol('x')
x_z3 = z3.Real('x')

def conditions(witness):
    """
    witness is expected to be a tuple: (f, T, y, x1, x2)
    where:
      f: a callable that takes a z3.Real and returns a z3 expression
      T: a strictly positive float (the period)
      y: a float (the target value)
      x1, x2: floats such that f(x1) < y < f(x2) or f(x2) < y < f(x1)
    """
    try:
        f, T, y, x1, x2 = witness
    except Exception:
        return [False, False, False]

    # H1: f is periodic with period T > 0
    try:
        T_float = float(T)
        if T_float <= 0:
            h1_ok = False
        else:
            x = z3.Real('x_var')
            solver = z3.Solver()
            solver.set("timeout", 2000)
            solver.add(f(x + T_float) != f(x))
            res = solver.check()
            h1_ok = (res == z3.unsat)
    except Exception:
        h1_ok = False

    # H2: inf(f) < y < sup(f)
    try:
        y_float = float(y)
        fx1 = f(z3.RealVal(float(x1)))
        fx2 = f(z3.RealVal(float(x2)))
        
        def check_less(val, target):
            s = z3.Solver()
            s.set("timeout", 1000)
            s.add(val < target)
            return s.check() == z3.sat
            
        def check_greater(val, target):
            s = z3.Solver()
            s.set("timeout", 1000)
            s.add(val > target)
            return s.check() == z3.sat

        cond_a = check_less(fx1, y_float) and check_greater(fx2, y_float)
        cond_b = check_greater(fx1, y_float) and check_less(fx2, y_float)
        
        h2_ok = cond_a or cond_b
    except Exception:
        h2_ok = False

    # Negated Conclusion: The set of points {x in R | f(x) = y} is finite.
    # For a periodic function with T > 0, the set of roots is finite iff it is empty.
    try:
        x = z3.Real('x_var')
        solver = z3.Solver()
        solver.set("timeout", 2000)
        solver.add(f(x) == float(y))
        res = solver.check()
        neg_q_ok = (res == z3.unsat)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is periodic with a strictly positive period T",
    "H_2: inf(f) < y < sup(f)",
    "¬Q: The set of points {x in R | f(x) = y} is finite"
]

N_HYP = 2
NEG_Q_INDEX = 2