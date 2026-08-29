import sympy
from sympy import Piecewise, Heaviside, Interval, S
from sympy.abc import x

# Top-level setup
# x is defined as a real symbol for use in witness expressions
x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            a = witness.get('a')
            b = witness.get('b')
        else:
            f, a, b = witness
    except Exception:
        return [False, False]

    # H_1: a < b
    try:
        h1_ok = bool(a < b)
    except Exception:
        h1_ok = False

    # neg_Q: For all c in (a, b), f(c) != (1 / (b - a)) * \int_a^b f(x) dx
    try:
        I = sympy.integrate(f, (x, a, b))
        
        # If the integral diverges or is undefined, the conclusion equation fails
        if I in [sympy.oo, -sympy.oo, sympy.zoo, sympy.nan] or I.is_finite is False:
            neg_q_ok = True
        else:
            target = I / (b - a)
            
            if sympy.simplify(f - target) == 0:
                neg_q_ok = False
            else:
                # Try solveset first
                sols = sympy.solveset(sympy.Eq(f, target), x, domain=sympy.Interval.open(a, b))
                
                if sols is sympy.S.EmptySet:
                    neg_q_ok = True
                elif isinstance(sols, sympy.Set) and not isinstance(sols, sympy.ConditionSet):
                    # It's a resolved set (FiniteSet, Interval, Union, etc.) and not empty
                    neg_q_ok = False
                else:
                    # Fallback to solve
                    sols_all = sympy.solve(sympy.Eq(f, target), x)
                    has_sol = False
                    for sol in sols_all:
                        try:
                            if sol.is_real and a < sol < b:
                                has_sol = True
                                break
                        except TypeError:
                            pass
                    
                    if not has_sol and isinstance(f, sympy.Piecewise):
                        all_const = True
                        for expr, cond in f.args:
                            if not expr.is_constant():
                                all_const = False
                                break
                            if sympy.simplify(expr - target) == 0:
                                has_sol = True
                        if all_const and not has_sol:
                            neg_q_ok = True
                        elif has_sol:
                            neg_q_ok = False
                        else:
                            neg_q_ok = True
                    else:
                        neg_q_ok = not has_sol
                    
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a < b",
    "¬Q: There is no c in (a, b) such that the integral of f from a to b equals f(c)(b - a)"
]

N_HYP = 1
NEG_Q_INDEX = 1