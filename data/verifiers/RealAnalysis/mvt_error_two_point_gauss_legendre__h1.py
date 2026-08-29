import sympy
from sympy.abc import x
import math

CONDITION_LABELS = [
    "¬Q: There is no c in (-1, 1) such that the error equals f^(4)(c)/135"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        f = witness
        
        # Compute the exact integral
        I = sympy.integrate(f, (x, -1, 1))
        
        # Compute the two-point Gauss-Legendre quadrature
        Q = f.subs(x, -1/sympy.sqrt(3)) + f.subs(x, 1/sympy.sqrt(3))
        
        # Compute the error
        E = sympy.simplify(I - Q)
        
        # Compute the fourth derivative
        f4 = sympy.diff(f, x, 4)
        
        # We want to check if there exists c in (-1, 1) such that E == f4(c) / 135.
        # If no such c exists, the conclusion fails (neg_q = True).
        eq = sympy.Eq(E, f4 / 135)
        
        if f4.is_constant():
            diff = sympy.simplify(E - f4/135)
            if diff == 0:
                neg_q = False
            else:
                try:
                    if abs(float(diff)) < 1e-9:
                        neg_q = False
                    else:
                        neg_q = True
                except Exception:
                    neg_q = True
        else:
            try:
                # Try to solve exactly in the interval (-1, 1)
                sols = sympy.solveset(eq, x, domain=sympy.Interval.open(-1, 1))
                if sols.is_empty == True:
                    neg_q = True
                elif sols.is_empty == False:
                    neg_q = False
                else:
                    raise ValueError("solveset could not determine if the solution set is empty")
            except Exception:
                # Fallback to general solve
                try:
                    roots = sympy.solve(eq, x)
                    has_sol = False
                    
                    if isinstance(roots, dict):
                        roots = [roots[x]]
                    elif len(roots) > 0 and isinstance(roots[0], dict):
                        roots = [d[x] for d in roots if x in d]
                        
                    for r in roots:
                        try:
                            r_val = float(r)
                            if -1 < r_val < 1:
                                has_sol = True
                                break
                        except Exception:
                            try:
                                if r.is_real and r > -1 and r < 1:
                                    has_sol = True
                                    break
                            except Exception:
                                pass
                    neg_q = not has_sol
                except Exception:
                    # Fallback to numerical sampling
                    try:
                        E_val = float(E)
                        has_sol = False
                        min_v = float('inf')
                        max_v = float('-inf')
                        
                        for i in range(1, 200):
                            c = -1 + 2 * i / 200
                            try:
                                v = float((f4 / 135).subs(x, c))
                                if not math.isnan(v):
                                    min_v = min(min_v, v)
                                    max_v = max(max_v, v)
                                    if abs(v - E_val) < 1e-7:
                                        has_sol = True
                                        break
                            except Exception:
                                pass
                                
                        if has_sol:
                            neg_q = False
                        else:
                            # If the required error is strictly outside the range of f4(c)/135,
                            # then no solution can exist.
                            if E_val < min_v - 1e-5 or E_val > max_v + 1e-5:
                                neg_q = True
                            else:
                                # Conservatively assume a solution might exist
                                neg_q = False
                    except Exception:
                        neg_q = False
    except Exception:
        neg_q = False

    return [neg_q]