import sympy as sp

x, y, z = sp.symbols('x y z')

def in_set(point, S_set):
    if callable(S_set):
        return bool(S_set(point))
    try:
        return bool(S_set.contains(point))
    except Exception:
        return False

def is_differentiable(expr, var, point):
    try:
        val = expr.subs(var, point)
        if val.is_real != True:
            return False
        deriv = expr.diff(var).subs(var, point)
        return deriv.is_real == True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        U = witness['U']
        V = witness['V']
        g = witness['g']
        f = witness['f']
        a = witness['a']
        var_g = witness.get('var_g', x)
        var_f = witness.get('var_f', x)
    except KeyError:
        return [False, False, False]

    try:
        h1_ok = in_set(a, U) and is_differentiable(g, var_g, a)
    except Exception:
        h1_ok = False

    try:
        ga = g.subs(var_g, a)
        h2_ok = in_set(ga, V) and is_differentiable(f, var_f, ga)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = False
        x_bad = witness.get('x_bad', None)
        
        if x_bad is not None:
            if in_set(x_bad, U) and not in_set(g.subs(var_g, x_bad), V):
                neg_q_ok = True
        
        if not neg_q_ok:
            fog = f.subs(var_f, g)
            if not is_differentiable(fog, var_g, a):
                neg_q_ok = True
            else:
                D_fog = fog.diff(var_g).subs(var_g, a)
                Df_ga = f.diff(var_f).subs(var_f, ga)
                Dg_a = g.diff(var_g).subs(var_g, a)
                if D_fog != Df_ga * Dg_a:
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: g is differentiable at a in U",
    "H_2: f is differentiable at g(a) in V",
    "¬Q: f o g is not a valid function from U to R^p, or not differentiable at a, or its derivative doesn't match"
]

N_HYP = 2
NEG_Q_INDEX = 2