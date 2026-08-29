import sympy as sp
import math
import itertools
import functools

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Parse witness
    if isinstance(witness, tuple):
        if len(witness) == 2:
            a_n, R_given = witness
        else:
            a_n = witness[0]
            R_given = None
        if isinstance(a_n, str):
            a_n = sp.sympify(a_n)
        if isinstance(R_given, str):
            R_given = sp.sympify(R_given)
    else:
        a_n = witness
        if isinstance(a_n, str):
            a_n = sp.sympify(a_n)
        R_given = None

    n_sym = sp.Symbol('n', integer=True, positive=True)
    if callable(a_n):
        try:
            a_n = a_n(n_sym)
        except Exception:
            pass

    if hasattr(a_n, 'free_symbols'):
        for s in a_n.free_symbols:
            if s.name == 'n':
                n_sym = s
                break

    def get_radius(seq, n_var):
        # Try ratio test
        try:
            ratio = sp.limit(sp.Abs(seq.subs(n_var, n_var+1) / seq), n_var, sp.oo)
            if ratio is not sp.nan:
                if ratio == 0:
                    return sp.oo
                elif ratio == sp.oo:
                    return 0
                else:
                    return 1 / ratio
        except Exception:
            pass
        # Try root test
        try:
            root = sp.limit(sp.Abs(seq)**(1/n_var), n_var, sp.oo)
            if root is not sp.nan:
                if root == 0:
                    return sp.oo
                elif root == sp.oo:
                    return 0
                else:
                    return 1 / root
        except Exception:
            pass
        return None

    neg_Q = False
    try:
        R_abs = get_radius(sp.Abs(a_n), n_sym)
        R_a = get_radius(a_n, n_sym)
        
        if R_given is not None:
            if R_abs is not None:
                try:
                    if sp.simplify(R_abs - R_given) != 0:
                        neg_Q = True
                except Exception:
                    if R_abs != R_given:
                        neg_Q = True
            
            # If the radius matches (or couldn't be computed), check the interval of convergence
            # as "radius of convergence" is sometimes loosely used to mean "interval of convergence".
            if not neg_Q and R_given != 0 and R_given != sp.oo:
                try:
                    conv_a_R = sp.Sum(a_n * (R_given**n_sym), (n_sym, 1, sp.oo)).is_convergent()
                    conv_a_mR = sp.Sum(a_n * ((-R_given)**n_sym), (n_sym, 1, sp.oo)).is_convergent()
                    conv_abs_R = sp.Sum(sp.Abs(a_n) * (R_given**n_sym), (n_sym, 1, sp.oo)).is_convergent()
                    conv_abs_mR = sp.Sum(sp.Abs(a_n) * ((-R_given)**n_sym), (n_sym, 1, sp.oo)).is_convergent()
                    
                    if conv_a_R in (True, False) and conv_abs_R in (True, False):
                        if conv_a_R != conv_abs_R:
                            neg_Q = True
                    if conv_a_mR in (True, False) and conv_abs_mR in (True, False):
                        if conv_a_mR != conv_abs_mR:
                            neg_Q = True
                except Exception:
                    pass
        else:
            if R_a is not None and R_abs is not None:
                try:
                    if sp.simplify(R_a - R_abs) != 0:
                        neg_Q = True
                except Exception:
                    if R_a != R_abs:
                        neg_Q = True
                        
            if not neg_Q and R_a is not None and R_a != 0 and R_a != sp.oo:
                try:
                    conv_a_R = sp.Sum(a_n * (R_a**n_sym), (n_sym, 1, sp.oo)).is_convergent()
                    conv_a_mR = sp.Sum(a_n * ((-R_a)**n_sym), (n_sym, 1, sp.oo)).is_convergent()
                    conv_abs_R = sp.Sum(sp.Abs(a_n) * (R_a**n_sym), (n_sym, 1, sp.oo)).is_convergent()
                    conv_abs_mR = sp.Sum(sp.Abs(a_n) * ((-R_a)**n_sym), (n_sym, 1, sp.oo)).is_convergent()
                    
                    if conv_a_R in (True, False) and conv_abs_R in (True, False):
                        if conv_a_R != conv_abs_R:
                            neg_Q = True
                    if conv_a_mR in (True, False) and conv_abs_mR in (True, False):
                        if conv_a_mR != conv_abs_mR:
                            neg_Q = True
                except Exception:
                    pass
    except Exception:
        pass

    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: The power series \\sum |a_n| x^n does not have the exact same radius of convergence R"
]

N_HYP = 0
NEG_Q_INDEX = 0