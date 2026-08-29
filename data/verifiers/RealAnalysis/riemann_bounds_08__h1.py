import sympy
from sympy import abc
import math

# Top-level setup
x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide p, a, b, f, g.
    """
    try:
        if isinstance(witness, dict):
            p = sympy.sympify(witness.get('p', 1), locals={'x': x})
            a = sympy.sympify(witness.get('a', 0), locals={'x': x})
            b = sympy.sympify(witness.get('b', 0), locals={'x': x})
            f = sympy.sympify(witness.get('f', 0), locals={'x': x})
            g = sympy.sympify(witness.get('g', 0), locals={'x': x})
        else:
            p, a, b, f, g = [sympy.sympify(v, locals={'x': x}) for v in witness]
    except Exception:
        return [False, False]
        
    # H_1: p >= 1
    try:
        h1 = bool(p >= 1)
    except Exception:
        h1 = False
        
    # ¬Q: Minkowski's inequality fails
    try:
        # Compute the integrals
        integrand_LHS = (sympy.Abs(f + g))**p
        int_LHS = sympy.integrate(integrand_LHS, (x, a, b))
        
        integrand_f = (sympy.Abs(f))**p
        int_f = sympy.integrate(integrand_f, (x, a, b))
        
        integrand_g = (sympy.Abs(g))**p
        int_g = sympy.integrate(integrand_g, (x, a, b))
        
        p_val = float(p.evalf())
        
        def get_root(val, p_v):
            c_val = complex(val.evalf())
            # Handle real roots for negative numbers when p is an odd integer
            if abs(c_val.imag) < 1e-9 and c_val.real < 0:
                if abs(p_v - round(p_v)) < 1e-9 and round(p_v) % 2 == 1:
                    return - ((-c_val.real) ** (1.0 / p_v))
            return c_val ** (1.0 / p_v)
            
        LHS_val = get_root(int_LHS, p_val)
        RHS_val = get_root(int_f, p_val) + get_root(int_g, p_val)
        
        # If the result is complex, the real inequality is invalid (fails)
        if abs(LHS_val.imag) > 1e-7 or abs(RHS_val.imag) > 1e-7:
            neg_q = True
        else:
            neg_q = not (LHS_val.real <= RHS_val.real + 1e-7)
            
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p >= 1",
    "¬Q: Minkowski's inequality fails"
]

N_HYP = 1
NEG_Q_INDEX = 1