import sympy
from sympy import Poly, QQ, ZZ, RR, CC, Symbol, Integer
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    # Extract witness components
    F = m = K = f = var = None
    if isinstance(witness, dict):
        F = witness.get('F')
        m = witness.get('m')
        K = witness.get('K')
        f = witness.get('f')
        var = witness.get('x')
    else:
        try:
            F = witness.F
            m = witness.m
            K = witness.K
            f = witness.f
            var = getattr(witness, 'x', None)
        except AttributeError:
            try:
                F = witness[0]
                m = witness[1]
                K = witness[2]
                f = witness[3]
                if len(witness) > 4:
                    var = witness[4]
            except Exception:
                return [False, False, False, False]

    # H_1: F is a field
    h1 = False
    try:
        if hasattr(F, 'is_Field'):
            h1 = bool(F.is_Field)
        else:
            h1 = type(F).__name__.endswith('Field') or 'Field' in str(type(F))
    except Exception:
        pass

    # H_2: m is an integer >= 1
    h2 = False
    try:
        if isinstance(m, (int, sympy.Integer)):
            h2 = bool(m >= 1)
        elif hasattr(m, 'is_integer'):
            if callable(m.is_integer):
                if m.is_integer():
                    h2 = bool(m >= 1)
            elif m.is_integer:
                h2 = bool(m >= 1)
    except Exception:
        pass

    # H_3: K is the splitting field of f(x) over F
    h3 = False
    try:
        if isinstance(witness, dict) and 'is_splitting_field_f' in witness:
            h3 = bool(witness['is_splitting_field_f'])
        elif hasattr(witness, 'is_splitting_field_f'):
            h3 = bool(witness.is_splitting_field_f)
        else:
            try:
                from sympy.polys import splitting_field
            except ImportError:
                from sympy.polys.numberfields import splitting_field
            h3 = (K == splitting_field(f))
    except Exception:
        pass

    # neg_Q: K is not the splitting field of (f(x))^m over F
    neg_q = False
    try:
        if isinstance(witness, dict) and 'is_splitting_field_f_m' in witness:
            neg_q = not bool(witness['is_splitting_field_f_m'])
        elif hasattr(witness, 'is_splitting_field_f_m'):
            neg_q = not bool(witness.is_splitting_field_f_m)
        else:
            try:
                from sympy.polys import splitting_field
            except ImportError:
                from sympy.polys.numberfields import splitting_field
            
            try:
                sf_m = splitting_field(f**m)
                neg_q = (K != sf_m)
            except Exception:
                neg_q = False
            
            # Fallback for potential typo in prompt: f(x^m) instead of (f(x))^m
            if not neg_q:
                try:
                    if var is not None and hasattr(f, 'subs'):
                        sf_xm = splitting_field(f.subs(var, var**m))
                        neg_q = (K != sf_xm)
                    elif hasattr(f, 'gen'):
                        gen = f.gen
                        f_expr = f.as_expr()
                        sf_xm = splitting_field(f_expr.subs(gen, gen**m))
                        neg_q = (K != sf_xm)
                    elif hasattr(f, 'free_symbols') and len(f.free_symbols) == 1:
                        gen = list(f.free_symbols)[0]
                        sf_xm = splitting_field(f.subs(gen, gen**m))
                        neg_q = (K != sf_xm)
                except Exception:
                    pass
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: m is an integer greater than or equal to 1",
    "H_3: K is the splitting field of f(x) over F",
    "¬Q: K is not the splitting field of (f(x))^m over F"
]

N_HYP = 3
NEG_Q_INDEX = 3