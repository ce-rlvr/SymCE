import sympy as sp

x, y, z = sp.symbols('x y z')

CONDITION_LABELS = [
    "¬Q: The equivalence between being a uniform limit of step functions and having one-sided limits everywhere fails"
]
N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        # Extract f, a, b from the witness
        if isinstance(witness, dict):
            f = witness.get('f', witness.get('expression', witness.get('func')))
            a = witness.get('a', 0)
            b = witness.get('b', 1)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                f, a, b = witness[0], witness[1], witness[2]
            elif len(witness) == 2:
                f = witness[0]
                try:
                    a, b = witness[1][0], witness[1][1]
                except Exception:
                    a, b = 0, 1
            else:
                f = witness[0]
                a, b = 0, 1
        elif hasattr(witness, 'f') and hasattr(witness, 'a') and hasattr(witness, 'b'):
            f = witness.f
            a = witness.a
            b = witness.b
        else:
            f = witness
            a, b = 0, 1

        if isinstance(f, str):
            f = sp.sympify(f)

        # Handle pure Python functions
        if callable(f) and not isinstance(f, sp.Basic):
            try:
                val_a = f(a)
            except Exception:
                val_a = None
            try:
                val_b = f(b)
            except Exception:
                val_b = None
                
            # If undefined at endpoints, it's not a uniform limit of step functions on [a, b]
            if val_a is None or val_b is None:
                return [True]
                
            # Check for infinite limits near endpoints
            try:
                if abs(f(a + 1e-9)) > 1e6 or abs(f(b - 1e-9)) > 1e6:
                    return [True]
            except Exception:
                return [True]
                
            return [False]

        if not isinstance(f, sp.Expr):
            return [False]

        symbols = list(f.free_symbols)
        sym = symbols[0] if symbols else sp.Symbol('x')

        # Check Side B: limits exist
        lim_a_right = sp.limit(f, sym, a, dir='+')
        lim_b_left = sp.limit(f, sym, b, dir='-')

        # If limits oscillate and don't exist, Side B is False, so equivalence holds (both False)
        if isinstance(lim_a_right, sp.AccumBounds) or isinstance(lim_b_left, sp.AccumBounds):
            return [False]

        # Check Side A: uniform limit of step functions
        # This requires f to be bounded and defined everywhere on [a, b]
        val_a = f.subs(sym, a)
        val_b = f.subs(sym, b)

        is_A_false = False
        if val_a.has(sp.nan, sp.zoo, sp.oo, -sp.oo) or val_b.has(sp.nan, sp.zoo, sp.oo, -sp.oo):
            is_A_false = True

        if lim_a_right in [sp.oo, -sp.oo, sp.zoo] or lim_b_left in [sp.oo, -sp.oo, sp.zoo]:
            is_A_false = True

        # If Side B is True (limits exist, possibly infinite) but Side A is False, equivalence fails
        if is_A_false:
            return [True]

        # Check for singularities inside (a, b)
        try:
            sings = sp.singularities(f, sym)
            for s in sings:
                if s.is_real and s > a and s < b:
                    lim_s_right = sp.limit(f, sym, s, dir='+')
                    lim_s_left = sp.limit(f, sym, s, dir='-')
                    if isinstance(lim_s_right, sp.AccumBounds) or isinstance(lim_s_left, sp.AccumBounds):
                        return [False]
                    if lim_s_right in [sp.oo, -sp.oo, sp.zoo] or lim_s_left in [sp.oo, -sp.oo, sp.zoo]:
                        return [True]
        except Exception:
            pass

        return [False]
    except Exception:
        return [False]