import sympy
from sympy import I, re, im, Abs, conjugate, Rational
import math
import itertools
import functools

# Top-level setup
QQ = sympy.polys.domains.QQ
RR = sympy.polys.domains.RR
CC = sympy.polys.domains.CC

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an algebraic closure of F",
    "H_3: \\sigma(a) = a for all a \\in F",
    "¬Q: \\sigma is not a bijective map or not an automorphism of E"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F_name = witness.get('F', 'R')
            E_name = witness.get('E', 'C')
            sigma = witness.get('sigma')
        elif callable(witness):
            F_name = 'R'
            E_name = 'C'
            sigma = witness
        else:
            F_name, E_name, sigma = witness
    except Exception:
        return [False, False, False, False]

    # H1: F is a field
    try:
        F_str = str(F_name)
        h1 = F_str in ['Q', 'R', 'C', 'QQ', 'RR', 'CC']
    except Exception:
        h1 = False

    # H2: E is an algebraic closure of F
    try:
        F_str = str(F_name)
        E_str = str(E_name)
        h2 = (F_str in ['R', 'RR'] and E_str in ['C', 'CC']) or \
             (F_str in ['Q', 'QQ'] and E_str in ['Q_bar', 'QQ_bar'])
    except Exception:
        h2 = False

    # H3: sigma(a) = a for all a in F
    try:
        test_vals = [sympy.S(0), sympy.S(1), sympy.S(-1), sympy.S(2), sympy.S(-2), 
                     sympy.Rational(1, 2), sympy.Rational(-1, 2), sympy.S(3), sympy.S(-3)]
        h3 = True
        for a in test_vals:
            val = sigma(a)
            try:
                diff = complex(val) - complex(a)
                if abs(diff) > 1e-7:
                    h3 = False
                    break
            except Exception:
                if sympy.simplify(val - a) != 0:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # neg_Q: sigma is not a bijective map or not an automorphism
    try:
        E_str = str(E_name)
        if E_str in ['C', 'CC']:
            e_vals = [I, -I, 1+I, 1-I, sympy.S(0), sympy.S(1), sympy.S(-1), 2*I, -2*I, sympy.S(2), sympy.S(-2)]
        elif E_str in ['Q_bar', 'QQ_bar']:
            e_vals = [I, -I, sympy.sqrt(2), -sympy.sqrt(2), sympy.S(0), sympy.S(1), sympy.S(-1)]
        else:
            e_vals = [sympy.S(0), sympy.S(1), sympy.S(-1)]
            
        is_injective = True
        seen = []
        for val in e_vals:
            res = sigma(val)
            for s in seen:
                try:
                    if abs(complex(res) - complex(s)) < 1e-7:
                        is_injective = False
                        break
                except Exception:
                    if sympy.simplify(res - s) == 0:
                        is_injective = False
                        break
            if not is_injective:
                break
            seen.append(res)
            
        is_homo = True
        for x_val in e_vals[:5]:
            for y_val in e_vals[:5]:
                try:
                    sum_val = sigma(x_val + y_val)
                    sum_parts = sigma(x_val) + sigma(y_val)
                    try:
                        if abs(complex(sum_val) - complex(sum_parts)) > 1e-7:
                            is_homo = False
                            break
                    except Exception:
                        if sympy.simplify(sum_val - sum_parts) != 0:
                            is_homo = False
                            break
                    
                    prod_val = sigma(x_val * y_val)
                    prod_parts = sigma(x_val) * sigma(y_val)
                    try:
                        if abs(complex(prod_val) - complex(prod_parts)) > 1e-7:
                            is_homo = False
                            break
                    except Exception:
                        if sympy.simplify(prod_val - prod_parts) != 0:
                            is_homo = False
                            break
                except Exception:
                    is_homo = False
                    break
            if not is_homo:
                break
                
        neg_q = (not is_injective) or (not is_homo)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]