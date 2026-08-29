import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy import Reals, Interval, Symbol
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: (X, d) is a metric space
    try:
        X = witness.get('X')
        if X is None:
            h1_ok = False
        elif hasattr(X, 'is_subset'):
            h1_ok = bool(X.is_subset(Reals))
        elif isinstance(X, (list, set, tuple)):
            h1_ok = all(isinstance(x, (int, float)) or (hasattr(x, 'is_real') and x.is_real) for x in X)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H2: S is a bounded subset of the real numbers
    try:
        S = witness.get('S')
        if S is None:
            h2_ok = False
        elif hasattr(S, 'is_subset') and hasattr(S, 'is_bounded'):
            h2_ok = bool(S.is_subset(Reals) and S.is_bounded)
        elif isinstance(S, (list, set, tuple)):
            h2_ok = all(isinstance(x, (int, float)) or (hasattr(x, 'is_real') and x.is_real) for x in S)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # neg_Q: The family of functions {c f | c in S, f in F} is NOT equicontinuous on X
    try:
        F = witness.get('F')
        if X is None or S is None or F is None:
            neg_q_ok = False
        else:
            # Find max |c| in S
            try:
                if isinstance(S, (list, set, tuple)):
                    if not S:
                        c_max = 0.0
                    else:
                        c_max = max(abs(float(c)) for c in S)
                else:
                    c_max = max(abs(float(S.sup)), abs(float(S.inf)))
            except Exception:
                c_max = 1.0
                
            if c_max == 0:
                neg_q_ok = False
            else:
                # Sample points in X
                try:
                    if hasattr(X, 'start') and hasattr(X, 'end'):
                        pts = []
                        try: pts.append(float(X.start))
                        except Exception: pass
                        try: pts.append(float(X.end))
                        except Exception: pass
                        try: pts.append(float((X.start + X.end)/2))
                        except Exception: pass
                        x_points = [p for p in pts if math.isfinite(p)]
                        if not x_points:
                            x_points = [0.0, 1.0, -1.0, 3.14]
                    elif isinstance(X, (list, set, tuple)):
                        x_points = []
                        for x in X:
                            try:
                                val = float(x)
                                if math.isfinite(val): x_points.append(val)
                            except Exception: pass
                        if not x_points:
                            x_points = [0.0, 1.0, -1.0, 3.14]
                    else:
                        x_points = [0.0, 1.0, -1.0, 3.14]
                except Exception:
                    x_points = [0.0, 1.0, -1.0, 3.14]
                    
                epsilon = 0.1
                deltas = [0.1, 0.01, 0.001, 0.0001, 0.00001]
                n_values = [1, 2, 5, 10, 50, 100, 500, 1000, 10000, 100000, 1000000]
                
                neg_q_ok = False
                for x0 in x_points:
                    try:
                        if hasattr(X, 'contains'):
                            if X.contains(x0) == False: continue
                        elif isinstance(X, (list, set, tuple)):
                            if x0 not in X: continue
                    except Exception:
                        pass
                        
                    x0_is_bad = True
                    for delta in deltas:
                        test_xs = [x0 + delta/2, x0 - delta/2, x0 + delta/10, x0 - delta/10]
                        found_large_diff = False
                        for x_val in test_xs:
                            try:
                                if hasattr(X, 'contains'):
                                    if X.contains(x_val) == False: continue
                                elif isinstance(X, (list, set, tuple)):
                                    if x_val not in X: continue
                            except Exception:
                                pass
                            
                            def get_vals():
                                if isinstance(F, (list, tuple, set)):
                                    for f in F:
                                        if hasattr(f, 'subs'):
                                            free = list(f.free_symbols)
                                            if free:
                                                var = free[0]
                                                try:
                                                    f_lam = sympy.lambdify(var, f, 'math')
                                                    yield float(f_lam(x_val)), float(f_lam(x0))
                                                except Exception:
                                                    try: yield float(f.subs(var, x_val)), float(f.subs(var, x0))
                                                    except Exception: pass
                                            else:
                                                try: yield float(f), float(f)
                                                except Exception: pass
                                        else:
                                            try: yield float(f(x_val)), float(f(x0))
                                            except Exception: pass
                                else:
                                    if hasattr(F, 'subs'):
                                        free = list(F.free_symbols)
                                        if len(free) == 1:
                                            var = free[0]
                                            try:
                                                f_lam = sympy.lambdify(var, F, 'math')
                                                yield float(f_lam(x_val)), float(f_lam(x0))
                                            except Exception:
                                                try: yield float(F.subs(var, x_val)), float(F.subs(var, x0))
                                                except Exception: pass
                                        elif len(free) >= 2:
                                            var_x, var_n = free[0], free[1]
                                            try:
                                                f_lam1 = sympy.lambdify((var_x, var_n), F, 'math')
                                                f_lam2 = sympy.lambdify((var_n, var_x), F, 'math')
                                                for n in n_values:
                                                    try: yield float(f_lam1(x_val, n)), float(f_lam1(x0, n))
                                                    except Exception: pass
                                                    try: yield float(f_lam2(x_val, n)), float(f_lam2(x0, n))
                                                    except Exception: pass
                                            except Exception:
                                                for n in n_values:
                                                    try: yield float(F.subs({var_x: x_val, var_n: n})), float(F.subs({var_x: x0, var_n: n}))
                                                    except Exception: pass
                                                    try: yield float(F.subs({var_n: x_val, var_x: n})), float(F.subs({var_n: x0, var_x: n}))
                                                    except Exception: pass
                                    else:
                                        try:
                                            yield float(F(x_val)), float(F(x0))
                                        except TypeError:
                                            for n in n_values:
                                                try: yield float(F(x_val, n)), float(F(x0, n))
                                                except Exception: pass
                                                try: yield float(F(n, x_val)), float(F(n, x0))
                                                except Exception: pass
                                        except Exception:
                                            pass

                            for val1, val2 in get_vals():
                                if abs(c_max * val1 - c_max * val2) > epsilon:
                                    found_large_diff = True
                                    break
                            if found_large_diff:
                                break
                        if not found_large_diff:
                            x0_is_bad = False
                            break
                    if x0_is_bad:
                        neg_q_ok = True
                        break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: S is a bounded subset of the real numbers",
    "¬Q: The family of functions {c f | c in S, f in F} is not equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2