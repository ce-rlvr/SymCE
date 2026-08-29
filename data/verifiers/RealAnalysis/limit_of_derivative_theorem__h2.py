import sympy
from sympy import Symbol, limit, diff, Interval, S, Piecewise
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary or tuple providing:
    f (SymPy expression), a, b, c, L (numbers/SymPy objects).
    """
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
            c = witness['c']
            L = witness['L']
        else:
            f, a, b, c, L = witness
    except Exception:
        return [False, False, False]

    # Determine the variable of the function
    try:
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            v = list(free_syms)[0]
        elif len(free_syms) > 1:
            v = next((sym for sym in free_syms if sym.name == 'x'), list(free_syms)[0])
        else:
            v = x
    except Exception:
        v = x

    # H_1: f is continuous on the interval
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        if a_sym >= b_sym:
            h1 = False
        else:
            dom = continuous_domain(f, v, S.Reals)
            h1_val = Interval(a_sym, b_sym).is_subset(dom)
            h1 = (h1_val == True)
    except Exception:
        h1 = False

    # H_2: The limit lim_{x->c} df/dx exists and equals L
    try:
        c_sym = sympy.sympify(c)
        L_sym = sympy.sympify(L)
        df = diff(f, v)
        lim_df_plus = limit(df, v, c_sym, dir='+')
        lim_df_minus = limit(df, v, c_sym, dir='-')
        h2 = bool(lim_df_plus == L_sym and lim_df_minus == L_sym)
    except Exception:
        h2 = False

    # ¬Q: f is not differentiable at c or df/dx at c != L
    try:
        val_c = f.subs(v, c_sym)
        if val_c.has(S.NaN, S.ComplexInfinity, S.Infinity, S.NegativeInfinity) or val_c.is_real is False:
            neg_q = True
        else:
            h = Symbol('h', real=True)
            diff_quotient = (f.subs(v, c_sym + h) - val_c) / h
            deriv_c_plus = limit(diff_quotient, h, 0, dir='+')
            deriv_c_minus = limit(diff_quotient, h, 0, dir='-')
            
            if deriv_c_plus != deriv_c_minus:
                neg_q = True
            elif deriv_c_plus.has(S.NaN, S.ComplexInfinity, S.Infinity, S.NegativeInfinity) or deriv_c_plus.is_real is False:
                neg_q = True
            else:
                neg_q = bool(deriv_c_plus != L_sym)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: f is continuous on the interval", "H_2: limit of derivative exists and equals L", "¬Q: f is not differentiable at c or derivative is not L"]
N_HYP = 2
NEG_Q_INDEX = 2