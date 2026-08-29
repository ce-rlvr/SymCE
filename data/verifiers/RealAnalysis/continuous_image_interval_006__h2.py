import sympy
from sympy import Symbol, Interval, solveset, EmptySet, S, Piecewise, sin, cos, tan, exp, log, floor, ceiling, sign
import z3
import math
import itertools
import functools

# Top-level setup for witness expressions
x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: I is an interval in the real numbers",
    "¬Q: The image f(I) is not an interval in the real numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        I, f = witness
    except Exception:
        return [False, False]
        
    # H1: I is an interval in the real numbers
    try:
        h1 = isinstance(I, Interval)
    except Exception:
        h1 = False
        
    # neg_Q: f(I) is NOT an interval
    neg_q = False
    try:
        if h1:
            # Determine sampling boundaries
            if I.start.is_finite and I.end.is_finite:
                start = float(I.start)
                end = float(I.end)
            else:
                start = float(I.start) if I.start.is_finite else -100.0
                end = float(I.end) if I.end.is_finite else 100.0
                
            # Generate sample points in the interval
            points = []
            for i in range(1001):
                p = start + i * (end - start) / 1000.0
                in_I = True
                if p < start or p > end:
                    in_I = False
                if p == start and I.left_open:
                    in_I = False
                if p == end and I.right_open:
                    in_I = False
                if in_I:
                    points.append(p)
                    
            # Prepare the function expression
            x_sym = Symbol('x', real=True)
            if callable(f):
                try:
                    f_expr = f(x_sym)
                except Exception:
                    f_expr = None
            else:
                f_expr = f
                
            # Evaluate the function at the sample points
            y_values = []
            for p in points:
                try:
                    if callable(f):
                        try:
                            val = float(f(p))
                            y_values.append(val)
                            continue
                        except Exception:
                            pass
                    if f_expr is not None:
                        val = float(f_expr.subs(x_sym, p))
                        y_values.append(val)
                except Exception:
                    pass
                    
            # Check for gaps in the image
            if len(y_values) >= 2:
                y_values = sorted(list(set(y_values)))
                gaps = []
                for i in range(len(y_values) - 1):
                    gaps.append((y_values[i+1] - y_values[i], y_values[i], y_values[i+1]))
                
                # Sort gaps by size descending
                gaps.sort(reverse=True, key=lambda item: item[0])
                
                y_mids_to_check = []
                # If the image crosses zero, zero is a prime candidate for a missing value
                if y_values[0] < 0 < y_values[-1]:
                    for gap_size, y1, y2 in gaps:
                        if y1 <= 0 <= y2:
                            y_mids_to_check.append(0.0)
                            break
                            
                # Check the midpoints of the largest gaps
                for gap_size, y1, y2 in gaps[:100]:
                    if gap_size > 1e-5:
                        y_mids_to_check.append((y1 + y2) / 2.0)
                        
                gap_found = False
                for y_mid in y_mids_to_check:
                    # 1. Try to prove the gap is real using sympy
                    if f_expr is not None:
                        try:
                            sol = solveset(f_expr - y_mid, x_sym, domain=I)
                            if sol == EmptySet:
                                gap_found = True
                                break
                        except Exception:
                            pass
                            
                    # 2. Try to prove the gap is real using Z3 (if callable)
                    if not gap_found and callable(f):
                        try:
                            x_z3 = z3.Real('x')
                            f_z3 = f(x_z3)
                            solver = z3.Solver()
                            solver.add(f_z3 == y_mid)
                            
                            if I.start.is_finite:
                                if I.left_open:
                                    solver.add(x_z3 > float(I.start))
                                else:
                                    solver.add(x_z3 >= float(I.start))
                            if I.end.is_finite:
                                if I.right_open:
                                    solver.add(x_z3 < float(I.end))
                                else:
                                    solver.add(x_z3 <= float(I.end))
                                    
                            if solver.check() == z3.unsat:
                                gap_found = True
                                break
                        except Exception:
                            pass
                            
                    if gap_found:
                        break
                        
                neg_q = gap_found
    except Exception:
        neg_q = False
        
    return [h1, neg_q]