import sympy
from sympy.abc import x, y, z

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    def get_attr(w, name, default=None):
        if isinstance(w, dict):
            return w.get(name, default)
        return getattr(w, name, default)

    def has_attr(w, name):
        if isinstance(w, dict):
            return name in w
        return hasattr(w, name)

    try:
        h1 = False
        try:
            K = get_attr(witness, 'K')
            if has_attr(K, 'is_Field') and K.is_Field:
                h1 = True
            elif has_attr(witness, 'is_field'):
                is_field = get_attr(witness, 'is_field')
                h1 = is_field() if callable(is_field) else is_field
            else:
                zero = get_attr(witness, 'zero', 0)
                one = get_attr(witness, 'one', 1)
                mul = get_attr(witness, 'mul', lambda a, b: a * b)
                h1 = True
                for a in K:
                    if a != zero:
                        if not any(mul(a, b) == one for b in K):
                            h1 = False
                            break
        except Exception:
            h1 = False

        h2 = False
        try:
            v = get_attr(witness, 'v')
            zero = get_attr(witness, 'zero', 0)
            add = get_attr(witness, 'add', lambda a, b: a + b)
            mul = get_attr(witness, 'mul', lambda a, b: a * b)
            
            test_elements = get_attr(witness, 'test_elements')
            if test_elements is None:
                K = get_attr(witness, 'K')
                if isinstance(K, (list, set, tuple)):
                    test_elements = list(K)
                else:
                    test_elements = [-2, -1, 0, 1, 2, sympy.Rational(1, 2), sympy.Rational(-1, 2)]
            
            h2 = True
            for a in test_elements:
                if a == zero: continue
                for b in test_elements:
                    if b == zero: continue
                    if v(mul(a, b)) != v(a) + v(b):
                        h2 = False
                    ab = add(a, b)
                    if ab != zero:
                        if v(ab) < min(v(a), v(b)):
                            h2 = False
        except Exception:
            h2 = False

        h3 = False
        try:
            R = get_attr(witness, 'R')
            def in_R(val):
                if callable(R): return R(val)
                return val in R
            
            h3 = True
            for a in test_elements:
                if a == zero:
                    if not in_R(a): h3 = False
                else:
                    if bool(v(a) >= 0):
                        if not in_R(a): h3 = False
                    else:
                        if in_R(a): h3 = False
        except Exception:
            h3 = False

        neg_q = False
        try:
            u = get_attr(witness, 'u')
            one = get_attr(witness, 'one', 1)
            mul = get_attr(witness, 'mul', lambda a, b: a * b)
            
            is_unit = False
            if in_R(u):
                if has_attr(witness, 'is_unit'):
                    is_unit_fn = get_attr(witness, 'is_unit')
                    is_unit = is_unit_fn(u) if callable(is_unit_fn) else is_unit_fn
                elif has_attr(witness, 'inv'):
                    inv_fn = get_attr(witness, 'inv')
                    is_unit = in_R(inv_fn(u))
                else:
                    try:
                        inv_u = one / u
                        is_unit = in_R(inv_u)
                    except Exception:
                        for b in test_elements:
                            if in_R(b) and mul(u, b) == one:
                                is_unit = True
                                break
                            
            v_u_is_zero = bool(v(u) == 0)
            
            neg_q = bool(is_unit) != v_u_is_zero
        except Exception:
            neg_q = False

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: v is a valuation on K with value group Gamma",
    "H_3: R is the valuation ring associated with v",
    "¬Q: u is a unit in R if and only if v(u) = 0 fails"
]

N_HYP = 3
NEG_Q_INDEX = 3