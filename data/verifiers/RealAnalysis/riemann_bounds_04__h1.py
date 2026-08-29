import sympy
from sympy import integrate, I, pi, E, oo
from sympy.abc import x, t, y, z

def conditions(witness) -> list[bool]:
    try:
        f_raw, g_raw, a_raw, b_raw = witness
        f = sympy.sympify(f_raw)
        g = sympy.sympify(g_raw)
        a = sympy.sympify(a_raw)
        b = sympy.sympify(b_raw)
        
        # Determine the variable of integration
        free_syms = f.free_symbols | g.free_symbols
        if not free_syms:
            var = x
        elif x in free_syms:
            var = x
        elif t in free_syms:
            var = t
        elif y in free_syms:
            var = y
        elif z in free_syms:
            var = z
        else:
            var = list(free_syms)[0]
            
        int_fg = integrate(f * g, (var, a, b))
        int_f2 = integrate(f**2, (var, a, b))
        int_g2 = integrate(g**2, (var, a, b))
        
        lhs = int_fg**2
        rhs = int_f2 * int_g2
        
        diff = sympy.simplify(lhs - rhs)
        
        try:
            diff_val = complex(diff.evalf())
            # If the difference is not purely real, the inequality is invalid (fails).
            if abs(diff_val.imag) > 1e-7:
                neg_q = True
            else:
                # If LHS > RHS, the <= inequality fails.
                neg_q = diff_val.real > 1e-7
        except TypeError:
            neg_q = False
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: (\\int_a^b f(x)g(x) dx)^2 <= (\\int_a^b f(x)^2 dx)(\\int_a^b g(x)^2 dx) fails"
]

N_HYP = 0
NEG_Q_INDEX = 0