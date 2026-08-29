import sympy
from sympy import symbols, diff, factor_list, Poly, sympify
from sympy.polys.polytools import groebner

x, y = symbols('x y')

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)):
            w_list = [witness]
        else:
            w_list = list(witness)
            
        h1 = True
        w_sym_list = []
        for w in w_list:
            w_sym = sympify(w, rational=True)
            if not w_sym.free_symbols.issubset({x, y}):
                h1 = False
                break
            if w_sym.has(sympy.I):
                h1 = False
                break
            Poly(w_sym, x, y)
            w_sym_list.append(w_sym)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            is_dedekind = True
            if len(w_sym_list) == 0:
                is_dedekind = False
            else:
                gb = groebner(w_sym_list, x, y)
                if len(gb) != 1:
                    is_dedekind = False
                else:
                    f = gb[0]
                    if f.is_number:
                        is_dedekind = False
                    else:
                        coeff, factors = factor_list(f)
                        if len(factors) > 1 or factors[0][1] > 1:
                            is_dedekind = False
                        else:
                            fx = diff(f, x)
                            fy = diff(f, y)
                            sing_gb = groebner([f, fx, fy], x, y)
                            if list(sing_gb) == [1]:
                                is_dedekind = True
                            else:
                                is_dedekind = False
            neg_q = not is_dedekind
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ['H_1: I is an ideal in the polynomial ring', '¬Q: the quotient ring is not a Dedekind domain']
N_HYP = 1
NEG_Q_INDEX = 1