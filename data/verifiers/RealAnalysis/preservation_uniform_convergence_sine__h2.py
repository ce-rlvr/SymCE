import sympy
import math

# Top-level setup: named object bindings that the witness expression may reference.
n = sympy.Symbol('n', integer=True, positive=True)
x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness should be a dictionary with:
      - 'f_n': sympy expression for f_n(x) in terms of n and x
      - 'f': sympy expression for f(x) in terms of x
      - 'X': sympy Set representing the domain
      - 'x_n': (optional) sympy expression for a sequence x_n in X to demonstrate non-uniform convergence
    """
    try:
        f_n = sympy.sympify(witness['f_n'])
        f = sympy.sympify(witness['f'])
        X = witness['X']
        
        # H_1: (f_n) is a sequence of real-valued functions defined on a set X
        h1 = isinstance(X, sympy.Set) and hasattr(f_n, 'subs') and hasattr(f, 'subs')
    except Exception:
        h1 = False

    try:
        neg_q = False
        if 'x_n' in witness:
            x_n = sympy.sympify(witness['x_n'])
            in_X = True
            # Verify that x_n is in X for sufficiently large n
            for test_n in [100, 1000, 10000]:
                val = x_n.subs(n, test_n)
                try:
                    if X.contains(val) == sympy.S.false or X.contains(val) == False:
                        in_X = False
                        break
                except Exception:
                    pass
            
            if in_X:
                # Check if sin(f_n(x_n)) - sin(f(x_n)) fails to converge to 0
                diff = sympy.sin(f_n.subs(x, x_n)) - sympy.sin(f.subs(x, x_n))
                try:
                    lim = sympy.limit(diff, n, sympy.oo)
                    if lim != 0:
                        neg_q = True
                except Exception:
                    # Fallback to numerical evaluation for large n
                    try:
                        val1 = float(diff.subs(n, 10000).evalf())
                        val2 = float(diff.subs(n, 20000).evalf())
                        if abs(val1) > 1e-4 or abs(val2) > 1e-4:
                            neg_q = True
                    except Exception:
                        pass
        else:
            # If x_n is not provided, check for pointwise non-convergence at some test points in X
            points_to_test = []
            if isinstance(X, sympy.Interval):
                if X.start != -sympy.oo:
                    points_to_test.append(X.start)
                if X.end != sympy.oo:
                    points_to_test.append(X.end)
                if X.start != -sympy.oo and X.end != sympy.oo:
                    points_to_test.append((X.start + X.end)/2)
                if X.start == -sympy.oo and X.end == sympy.oo:
                    points_to_test.extend([0, 1, -1, sympy.pi])
            else:
                points_to_test.append(0)
                
            for pt in points_to_test:
                diff = sympy.sin(f_n.subs(x, pt)) - sympy.sin(f.subs(x, pt))
                try:
                    lim = sympy.limit(diff, n, sympy.oo)
                    if lim != 0:
                        neg_q = True
                        break
                except Exception:
                    try:
                        val = float(diff.subs(n, 10000).evalf())
                        if abs(val) > 1e-4:
                            neg_q = True
                            break
                    except Exception:
                        pass
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of real-valued functions defined on a set X",
    "¬Q: sin(f_n(x)) does not converge uniformly to sin(f(x)) on X"
]

N_HYP = 1
NEG_Q_INDEX = 1