import sympy as sp
from sympy import limit, Interval, Intersection, S, Rational
from sympy.calculus.util import continuous_domain
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            x_sym = witness['x']
            a = witness['a']
            b = witness['b']
            c = witness['c']
            domain = witness.get('domain', S.Reals)
        elif hasattr(witness, 'f'):
            f = witness.f
            x_sym = witness.x
            a = witness.a
            b = witness.b
            c = witness.c
            domain = getattr(witness, 'domain', S.Reals)
        else:
            if len(witness) == 6:
                f, x_sym, domain, a, b, c = witness
            elif len(witness) == 5:
                f, x_sym, a, b, c = witness
                domain = S.Reals
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        nat_domain = continuous_domain(f, x_sym, S.Reals)
        actual_domain = Intersection(domain, nat_domain)
    except Exception:
        actual_domain = domain

    # H1: c in (a, b) is a local extremum of f
    try:
        h1_part1 = bool((c > a) and (c < b))
        
        h1_part2 = False
        try:
            neighborhood = Intersection(actual_domain, Interval(c - Rational(1, 10), c + Rational(1, 10)))
            min_val = sp.minimum(f, x_sym, neighborhood)
            max_val = sp.maximum(f, x_sym, neighborhood)
            c_val = f.subs(x_sym, c)
            if min_val == c_val or max_val == c_val:
                h1_part2 = True
        except Exception:
            pass
            
        if not h1_part2:
            try:
                c_val_c = complex(f.subs(x_sym, c))
                if c_val_c.imag == 0:
                    c_val = c_val_c.real
                    is_min = True
                    is_max = True
                    for eps in [1e-5, 1e-4, 1e-3]:
                        for sign in [-1, 1]:
                            pt = c + sign * eps
                            if actual_domain.contains(pt) == True:
                                val = complex(f.subs(x_sym, pt))
                                if val.imag != 0:
                                    continue
                                val = val.real
                                if val < c_val:
                                    is_min = False
                                if val > c_val:
                                    is_max = False
                    h1_part2 = is_min or is_max
            except Exception:
                h1_part2 = False
                
        h1_ok = bool(h1_part1 and h1_part2)
    except Exception:
        h1_ok = False

    # H2: f is differentiable at c
    try:
        if actual_domain.contains(c) != True:
            h2_ok = False
            deriv_val = None
        else:
            dq = (f - f.subs(x_sym, c)) / (x_sym - c)
            
            left_in = (Intersection(actual_domain, Interval.open(c - 1, c)).is_empty == False)
            if left_in:
                pt = c - 1e-5
                if actual_domain.contains(pt) == True:
                    try:
                        if complex(f.subs(x_sym, pt)).imag != 0:
                            left_in = False
                    except Exception:
                        pass

            right_in = (Intersection(actual_domain, Interval.open(c, c + 1)).is_empty == False)
            if right_in:
                pt = c + 1e-5
                if actual_domain.contains(pt) == True:
                    try:
                        if complex(f.subs(x_sym, pt)).imag != 0:
                            right_in = False
                    except Exception:
                        pass
            
            L_left = None
            L_right = None
            
            if left_in:
                L_left = limit(dq, x_sym, c, dir='-')
            if right_in:
                L_right = limit(dq, x_sym, c, dir='+')
                
            if left_in and right_in:
                h2_ok = bool(L_left.is_real and L_right.is_real and L_left == L_right)
                deriv_val = L_left
            elif left_in:
                h2_ok = bool(L_left.is_real)
                deriv_val = L_left
            elif right_in:
                h2_ok = bool(L_right.is_real)
                deriv_val = L_right
            else:
                h2_ok = False
                deriv_val = None
    except Exception:
        h2_ok = False
        deriv_val = None

    # neg_Q: f'(c) != 0
    try:
        if h2_ok and deriv_val is not None:
            is_z = sp.simplify(deriv_val).is_zero
            if is_z is None:
                neg_q_ok = float(deriv_val) != 0.0
            else:
                neg_q_ok = not is_z
        else:
            formal_deriv = sp.diff(f, x_sym).subs(x_sym, c)
            is_z = sp.simplify(formal_deriv).is_zero
            if is_z is None:
                neg_q_ok = float(formal_deriv) != 0.0
            else:
                neg_q_ok = not is_z
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: c in (a, b) is a local extremum (maximum or minimum) of f",
    "H_2: f is differentiable at c",
    "¬Q: f'(c) != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2