import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

x = sympy.Symbol('x', real=True)
c = sympy.Symbol('c', real=True)

def parse_witness(witness):
    if isinstance(witness, dict):
        return witness['f'], witness['g'], witness['a'], witness['b']
    return witness[0], witness[1], witness[2], witness[3]

def conditions(witness) -> list[bool]:
    try:
        f, g, a, b = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    # H1: g is monotonically decreasing on the interval
    h1_ok = False
    h1_resolved = False
    try:
        deriv = sympy.diff(g, x)
        pos_sols = sympy.solveset(deriv > 0, x, domain=sympy.Interval(a, b))
        if pos_sols == sympy.EmptySet:
            h1_ok = True
            h1_resolved = True
        elif pos_sols.is_empty == False:
            h1_ok = False
            h1_resolved = True
    except Exception:
        pass
        
    if not h1_resolved:
        try:
            pts = [a + (b - a) * i / 100.0 for i in range(101)]
            vals = [float(g.subs(x, p)) for p in pts]
            h1_ok = True
            for i in range(100):
                if vals[i] < vals[i+1] - 1e-7:
                    h1_ok = False
                    break
        except Exception:
            h1_ok = False

    # H2: g(x) >= 0 for all x in the interval
    h2_ok = False
    h2_resolved = False
    try:
        neg_sols = sympy.solveset(g < 0, x, domain=sympy.Interval(a, b))
        if neg_sols == sympy.EmptySet:
            h2_ok = True
            h2_resolved = True
        elif neg_sols.is_empty == False:
            h2_ok = False
            h2_resolved = True
    except Exception:
        pass
        
    if not h2_resolved:
        try:
            pts = [a + (b - a) * i / 100.0 for i in range(101)]
            vals = [float(g.subs(x, p)) for p in pts]
            if all(v >= -1e-7 for v in vals):
                h2_ok = True
        except Exception:
            h2_ok = False

    # neg_Q: Conclusion fails
    neg_q_ok = False
    try:
        LHS_expr = sympy.Integral(f * g, (x, a, b))
        LHS_val = LHS_expr.evalf()
        if not LHS_val.is_real or not LHS_val.is_finite:
            neg_q_ok = True
    except Exception:
        neg_q_ok = True

    if not neg_q_ok:
        resolved = False
        try:
            ga_val = float(g.subs(x, a))
            LHS_sym = sympy.integrate(f * g, (x, a, b))
            RHS_sym = g.subs(x, a) * sympy.integrate(f, (x, a, c))
            
            if not LHS_sym.has(sympy.Integral) and not RHS_sym.has(sympy.Integral):
                eq = sympy.Eq(LHS_sym, RHS_sym)
                sols = sympy.solveset(eq, c, domain=sympy.Interval(a, b))
                if sols == sympy.EmptySet:
                    neg_q_ok = True
                    resolved = True
                elif sols.is_empty == False:
                    neg_q_ok = False
                    resolved = True
        except Exception:
            pass

        if not resolved:
            try:
                LHS_num = float(LHS_val)
                min_diff = float('inf')
                
                F = sympy.integrate(f, x)
                has_indefinite = not F.has(sympy.Integral)
                if has_indefinite:
                    F_a = F.subs(x, a)
                    
                found_c = False
                for i in range(101):
                    c_val = a + (b - a) * i / 100.0
                    if has_indefinite:
                        try:
                            RHS_val = ga_val * float(F.subs(x, c_val) - F_a)
                        except Exception:
                            continue
                    else:
                        if i % 5 != 0:
                            continue
                        try:
                            RHS_expr = sympy.Integral(f, (x, a, c_val))
                            RHS_val = ga_val * float(RHS_expr.evalf())
                        except Exception:
                            continue
                            
                    diff = abs(LHS_num - RHS_val)
                    if diff < 1e-4:
                        found_c = True
                        break
                    if diff < min_diff:
                        min_diff = diff
                        
                if not found_c and min_diff > 1e-3:
                    neg_q_ok = True
            except Exception:
                neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: g is monotonically decreasing",
    "H_2: g(x) >= 0",
    "¬Q: Conclusion fails"
]

N_HYP = 2
NEG_Q_INDEX = 2