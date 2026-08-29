import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy.abc import x
import math
import itertools
import functools

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
    try:
        f_expr, points = witness
        f_expr = sympy.sympify(f_expr)
        if not isinstance(points, (list, tuple)):
            return [False, False]
        if len(points) < 2:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        points = [sympy.sympify(p) for p in points]
        if any(p.is_real is False for p in points):
            h1 = False
        else:
            float_points = []
            for p in points:
                float_points.append(float(p.evalf()))
            h1 = len(set(float_points)) == len(float_points)
    except Exception:
        h1 = False

    try:
        n = len(points) - 1
        a = points[float_points.index(min(float_points))]
        b = points[float_points.index(max(float_points))]
        
        free_syms = f_expr.free_symbols
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
        else:
            sym = x
            
        div_diff = 0
        for j in range(n + 1):
            term = f_expr.subs(sym, points[j])
            denom = 1
            for k in range(n + 1):
                if k != j:
                    denom *= (points[j] - points[k])
            div_diff += term / denom
        div_diff = sympy.simplify(div_diff)
        
        f_n = sympy.diff(f_expr, sym, n)
        eq = f_n / sympy.factorial(n) - div_diff
        
        has_solution = False
        try:
            sols_set = sympy.solveset(eq, sym, domain=sympy.Interval.open(a, b))
            if sols_set == sympy.S.EmptySet:
                has_solution = False
            elif isinstance(sols_set, sympy.FiniteSet):
                for sol in sols_set:
                    try:
                        val = f_n.subs(sym, sol)
                        if val.is_real is not False and not val.has(sympy.nan, sympy.zoo, sympy.oo, -sympy.oo):
                            has_solution = True
                            break
                    except Exception:
                        pass
            elif isinstance(sols_set, sympy.ConditionSet):
                raise ValueError("ConditionSet")
            else:
                if sols_set.is_empty == False:
                    has_solution = True
                elif sols_set.is_empty == True:
                    has_solution = False
                else:
                    raise ValueError("Cannot determine if set is empty")
        except Exception:
            try:
                sols = sympy.solve(eq, sym)
                if isinstance(sols, dict):
                    sols = list(sols.keys())
                for sol in sols:
                    try:
                        sol_float = float(sol.evalf())
                        if float(a.evalf()) < sol_float < float(b.evalf()):
                            val = f_n.subs(sym, sol)
                            if val.is_real is not False and not val.has(sympy.nan, sympy.zoo, sympy.oo, -sympy.oo):
                                has_solution = True
                                break
                    except Exception:
                        pass
            except Exception:
                pass
                
        neg_q = not has_solution
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x_0, x_1, ..., x_n are distinct points",
    "not_Q: There is no c in (min(x_i), max(x_i)) such that divided_difference = f^(n)(c) / n!"
]

N_HYP = 1
NEG_Q_INDEX = 1