import sympy
from sympy import Piecewise, Interval, Eq, solveset, integrate, S

x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    witness: tuple (f, a, b)
    where f is a sympy expression in terms of x (or a callable),
    and a, b are real numbers defining the interval.
    """
    try:
        f, a, b = witness
        
        if callable(f):
            f = f(x)
            
        # The interval must be valid and non-empty
        if float(a) >= float(b):
            return [False]
            
        # Compute the definite integral
        I = integrate(f, (x, a, b))
        
        # Reject if the integral is undefined or infinite
        if I.has(sympy.oo, sympy.zoo, sympy.nan, -sympy.oo):
            return [False]
            
        # Compute the average value
        avg = I / (b - a)
        
        # Check if there exists c in the interval such that f(c) == avg
        sols = solveset(Eq(f, avg), x, domain=Interval(a, b))
        
        if sols is S.EmptySet:
            neg_q = True
        else:
            neg_q = False
            # Fallback for piecewise constant functions if solveset returns a ConditionSet
            if isinstance(f, Piecewise):
                possible_values = set()
                is_constant_piecewise = True
                for expr, cond in f.args:
                    if expr.is_constant():
                        possible_values.add(expr)
                    else:
                        is_constant_piecewise = False
                        break
                
                if is_constant_piecewise:
                    match_found = False
                    for val in possible_values:
                        if sympy.simplify(val - avg) == 0:
                            match_found = True
                            break
                    if not match_found:
                        neg_q = True
            
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = ["¬Q: There is no c in the interval such that the integral of f equals f(c)(b-a)"]

N_HYP = 0
NEG_Q_INDEX = 0