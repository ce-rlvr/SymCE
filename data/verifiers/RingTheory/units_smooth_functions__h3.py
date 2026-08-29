import sympy as sp

# Setup the environment
x = sp.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: M is a smooth manifold",
    "H_2: C^infty(M) is the ring of smooth real-valued functions on M",
    "¬Q: The equivalence 'f is a unit in C^infty(M) iff f(p) != 0 for all p' fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # If the witness is provided as a string, sympify it
    if isinstance(witness, str):
        try:
            witness = sp.sympify(witness, locals={'x': x})
        except Exception:
            return [False, False, False]
            
    # If the witness is a callable (e.g., lambda function), evaluate it at x
    if callable(witness):
        try:
            witness = witness(x)
        except Exception:
            return [False, False, False]

    # H1 and H2 are context setup for the manifold M = Reals
    h1 = True
    h2 = True
    
    # Evaluate RHS of the conclusion: f(p) != 0 for all p in M
    try:
        roots = sp.solveset(witness, x, domain=sp.S.Reals)
        if roots.is_empty is True:
            rhs = True
        elif roots.is_empty is False:
            rhs = False
        else:
            # Fallback numerical check if solveset cannot decide
            rhs = True
            for i in range(-1000, 1000):
                val = i / 100.0
                try:
                    if abs(float(witness.subs(x, val))) < 1e-6:
                        rhs = False
                        break
                except Exception:
                    pass
    except Exception:
        rhs = False

    # Evaluate LHS of the conclusion: f is a unit in C^infty(M)
    # This means f is smooth AND 1/f is smooth.
    try:
        def is_smooth(f, var):
            # Reject functions with obvious non-smooth trigonometric asymptotes
            if f.has(sp.tan) or f.has(sp.sec) or f.has(sp.cot) or f.has(sp.csc):
                if not f.is_constant():
                    return False
            
            derivs = [f]
            for _ in range(3):
                derivs.append(derivs[-1].diff(var))
            
            # Collect suspicious points where non-smoothness might occur
            points = set()
            for arg in f.atoms(sp.Abs):
                g = arg.args[0]
                rts = sp.solveset(g, var, domain=sp.S.Reals)
                if isinstance(rts, sp.FiniteSet):
                    points.update(rts)
            for arg in f.atoms(sp.sign):
                g = arg.args[0]
                rts = sp.solveset(g, var, domain=sp.S.Reals)
                if isinstance(rts, sp.FiniteSet):
                    points.update(rts)
            for arg in f.atoms(sp.Pow):
                base, exp = arg.args
                if exp.is_rational and not exp.is_integer:
                    rts = sp.solveset(base, var, domain=sp.S.Reals)
                    if isinstance(rts, sp.FiniteSet):
                        points.update(rts)
                if exp.is_number and exp < 0:
                    rts = sp.solveset(base, var, domain=sp.S.Reals)
                    if isinstance(rts, sp.FiniteSet):
                        points.update(rts)
            for arg in f.atoms(sp.Max, sp.Min):
                for a in arg.args:
                    for b in arg.args:
                        if a != b:
                            rts = sp.solveset(a - b, var, domain=sp.S.Reals)
                            if isinstance(rts, sp.FiniteSet):
                                points.update(rts)
            for arg in f.atoms(sp.Piecewise):
                for expr, cond in arg.args:
                    for rel in cond.atoms(sp.Relational):
                        lhs_rel, rhs_rel = rel.args
                        rts = sp.solveset(lhs_rel - rhs_rel, var, domain=sp.S.Reals)
                        if isinstance(rts, sp.FiniteSet):
                            points.update(rts)
            for arg in f.atoms(sp.log):
                g = arg.args[0]
                rts = sp.solveset(g, var, domain=sp.S.Reals)
                if isinstance(rts, sp.FiniteSet):
                    points.update(rts)
                points.add(sp.S(0))
            points.add(sp.S(0))
            
            # Check limits of the function and its derivatives at suspicious points
            for pt in points:
                for df in derivs:
                    if df.has(sp.DiracDelta) or df.has(sp.Heaviside):
                        return False
                    try:
                        L = sp.limit(df, var, pt, dir='-')
                        R = sp.limit(df, var, pt, dir='+')
                        if L != R or L.has(sp.oo, -sp.oo, sp.zoo, sp.nan) or not L.is_number or not R.is_number:
                            return False
                    except Exception:
                        # Fallback numerical limit check
                        try:
                            val_L = float(df.subs(var, pt - 1e-5))
                            val_R = float(df.subs(var, pt + 1e-5))
                            if abs(val_L - val_R) > 1e-2:
                                return False
                        except Exception:
                            return False
            return True

        f_smooth = is_smooth(witness, x)
        if not f_smooth:
            lhs = False
        else:
            inv_f_smooth = is_smooth(1/witness, x)
            lhs = inv_f_smooth
    except Exception:
        lhs = False

    # The conclusion fails if the equivalence does not hold
    neg_q = (lhs != rhs)
    
    return [h1, h2, neg_q]