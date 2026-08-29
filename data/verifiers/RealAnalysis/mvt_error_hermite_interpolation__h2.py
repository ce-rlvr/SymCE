import sympy as sp
from sympy.abc import t
import math
import itertools
import functools

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        f = sp.sympify(witness['f'])
        a = sp.sympify(witness['a'])
        b = sp.sympify(witness['b'])
        nodes = [sp.sympify(node) for node in witness['nodes']]
        x_val = sp.sympify(witness['x'])
        n = len(nodes)
        if n < 1:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: f is 2n times continuously differentiable on the interval
    try:
        if not (a < b):
            h1 = False
        else:
            f_diff = sp.diff(f, t, 2*n)
            h1 = True
            
            # Check for poles in rational functions
            denom = sp.fraction(sp.cancel(f))[1]
            roots = sp.solve(denom, t)
            for r in roots:
                try:
                    r_val = complex(r.evalf())
                    if abs(r_val.imag) < 1e-7:
                        if float(a) <= r_val.real <= float(b):
                            h1 = False
                            break
                except Exception:
                    pass
                    
            # Heuristic check: evaluate at 11 points to ensure no singularities
            if h1:
                for i in range(11):
                    pt = float(a) + i * (float(b) - float(a)) / 10.0
                    try:
                        v1 = complex(f.subs(t, pt).evalf())
                        v2 = complex(f_diff.subs(t, pt).evalf())
                        if abs(v1.imag) > 1e-7 or abs(v2.imag) > 1e-7:
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: x is not one of the interpolation nodes
    try:
        a_val = float(a)
        b_val = float(b)
        x_val_f = float(x_val)
        
        h2 = (a_val <= x_val_f <= b_val)
        
        for node in nodes:
            if abs(x_val_f - float(node)) < 1e-7:
                h2 = False
                break
    except Exception:
        h2 = False

    # neg_Q: There does NOT exist c in the interval such that the error formula holds
    try:
        degree = 2 * n - 1
        coeffs = sp.symbols(f'c0:{degree+1}')
        P = sum(c * t**i for i, c in enumerate(coeffs))
        P_prime = sp.diff(P, t)
        
        f_prime = sp.diff(f, t)
        
        eqs = []
        for node in nodes:
            eqs.append(P.subs(t, node) - f.subs(t, node))
            eqs.append(P_prime.subs(t, node) - f_prime.subs(t, node))
            
        sol = sp.solve(eqs, coeffs, dict=True)
        if not sol or len(sol[0]) < degree + 1:
            neg_q = False
        else:
            P_sol = P.subs(sol[0])
            
            E = f.subs(t, x_val) - P_sol.subs(t, x_val)
            
            W = 1
            for node in nodes:
                W *= (x_val - node)**2
                
            if W == 0:
                # If W == 0, x is a node, E is 0, 0 = 0 holds for any c.
                neg_q = False
            else:
                V = E * sp.factorial(2*n) / W
                
                f_2n = sp.diff(f, t, 2*n)
                
                f_2n_simp = sp.simplify(f_2n)
                V_simp = sp.simplify(V)
                
                if V_simp.free_symbols:
                    neg_q = False
                elif t not in f_2n_simp.free_symbols:
                    val = complex(f_2n_simp.evalf())
                    V_val = complex(V_simp.evalf())
                    if abs(val - V_val) < 1e-7:
                        # Equation is 0 == 0, all c are solutions.
                        neg_q = False
                    else:
                        # Equation is 1 == 0, no solutions.
                        neg_q = True
                else:
                    eq = sp.Eq(f_2n_simp, V_simp)
                    sols = sp.solve(eq, t)
                    
                    has_solution_in_interval = False
                    for sol_c in sols:
                        try:
                            c_val = complex(sol_c.evalf())
                            if abs(c_val.imag) < 1e-7:
                                if float(a) < c_val.real < float(b):
                                    has_solution_in_interval = True
                                    break
                        except Exception:
                            pass
                            
                    if not has_solution_in_interval:
                        # Double check with IVT in case sp.solve missed a root
                        try:
                            diff_func = f_2n_simp - V_simp
                            signs = set()
                            for i in range(101):
                                pt = float(a) + i * (float(b) - float(a)) / 100.0
                                val = complex(diff_func.subs(t, pt).evalf())
                                if abs(val.imag) < 1e-7:
                                    if val.real > 1e-7:
                                        signs.add(1)
                                    elif val.real < -1e-7:
                                        signs.add(-1)
                                    else:
                                        has_solution_in_interval = True
                                        break
                            if 1 in signs and -1 in signs:
                                has_solution_in_interval = True
                        except Exception:
                            pass
                            
                    neg_q = not has_solution_in_interval
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is 2n times continuously differentiable on the interval",
    "H_2: x is not one of the interpolation nodes",
    "neg_Q: There does NOT exist c in the interval such that the error formula holds"
]

N_HYP = 2
NEG_Q_INDEX = 2