import sympy as sp

x = sp.Symbol('x', real=True)

def conditions(witness):
    """
    witness is expected to be a tuple of 4 sympy expressions: (f, g, f_star, g_star)
    representing functions of the variable `x`.
    """
    try:
        f, g, f_star, g_star = witness
        
        # H_1: f* and g* are the symmetric decreasing rearrangements of f and g
        # 1. Check symmetry: f*(x) == f*(-x)
        sym_f = sp.simplify(f_star - f_star.subs(x, -x)) == 0
        sym_g = sp.simplify(g_star - g_star.subs(x, -x)) == 0
        
        # 2. Check decreasing for x > 0
        df = sp.diff(f_star, x)
        dg = sp.diff(g_star, x)
        dec_f = all(float(df.subs(x, v)) <= 1e-5 for v in [0.5, 1.0, 2.0])
        dec_g = all(float(dg.subs(x, v)) <= 1e-5 for v in [0.5, 1.0, 2.0])
        
        # 3. Check equimeasurability (via moments)
        int_f = sp.integrate(f, (x, -sp.oo, sp.oo))
        int_f_star = sp.integrate(f_star, (x, -sp.oo, sp.oo))
        eq_f1 = abs(float(int_f) - float(int_f_star)) < 1e-5
        
        int_f2 = sp.integrate(f**2, (x, -sp.oo, sp.oo))
        int_f_star2 = sp.integrate(f_star**2, (x, -sp.oo, sp.oo))
        eq_f2 = abs(float(int_f2) - float(int_f_star2)) < 1e-5
        
        int_g = sp.integrate(g, (x, -sp.oo, sp.oo))
        int_g_star = sp.integrate(g_star, (x, -sp.oo, sp.oo))
        eq_g1 = abs(float(int_g) - float(int_g_star)) < 1e-5
        
        int_g2 = sp.integrate(g**2, (x, -sp.oo, sp.oo))
        int_g_star2 = sp.integrate(g_star**2, (x, -sp.oo, sp.oo))
        eq_g2 = abs(float(int_g2) - float(int_g_star2)) < 1e-5
        
        h1 = sym_f and sym_g and dec_f and dec_g and eq_f1 and eq_f2 and eq_g1 and eq_g2
        
        # Conclusion: int f g <= int f* g*
        # Negated conclusion: int f g > int f* g*
        int_fg = sp.integrate(f * g, (x, -sp.oo, sp.oo))
        int_fstar_gstar = sp.integrate(f_star * g_star, (x, -sp.oo, sp.oo))
        
        neg_q = float(int_fg) > float(int_fstar_gstar) + 1e-5
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: f* and g* are the symmetric decreasing rearrangements of f and g respectively",
    "¬Q: The integral of f*g is strictly less than the integral of f*g*"
]

N_HYP = 1
NEG_Q_INDEX = 1