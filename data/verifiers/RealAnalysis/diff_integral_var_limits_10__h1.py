import sympy

t = sympy.Symbol('t', real=True)
x = sympy.Symbol('x', real=True)
y = sympy.Symbol('y', real=True)

def conditions(witness):
    # H_1: F is defined by the integral. We check if it's integrable on [-1, 1].
    try:
        val1 = sympy.integrate(witness, (t, 0, 1))
        val2 = sympy.integrate(witness, (t, -1, 0))
        if val1.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan) or \
           val2.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan):
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    neg_q = False
    try:
        test_points = [-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0]
        
        # Extract potential points of discontinuity from Piecewise conditions
        if isinstance(witness, sympy.Piecewise):
            for expr, cond in witness.args:
                for rel in cond.atoms(sympy.Relational):
                    try:
                        roots = sympy.solve(rel.lhs - rel.rhs, t, dict=True)
                        for d in roots:
                            if t in d:
                                r = d[t]
                                if r.is_real:
                                    test_points.append(float(r))
                    except Exception:
                        pass
        
        # Extract potential points of discontinuity from Heaviside and sign functions
        for func in [sympy.Heaviside, sympy.sign]:
            if witness.has(func):
                for arg in witness.atoms(func):
                    try:
                        roots = sympy.solve(arg.args[0], t, dict=True)
                        for d in roots:
                            if t in d:
                                r = d[t]
                                if r.is_real:
                                    test_points.append(float(r))
                    except Exception:
                        pass
                    
        # Remove duplicates and sort
        test_points = sorted(list(set([round(p, 5) for p in test_points])))
        
        h = sympy.Symbol('h', real=True)
        
        for z in test_points:
            try:
                fz = witness.subs(t, z)
                
                # Check if the function is continuous at z
                lim_plus = sympy.limit(witness, t, z, '+')
                lim_minus = sympy.limit(witness, t, z, '-')
                
                if lim_plus == lim_minus == fz:
                    continue
            except Exception:
                pass
            
            # If not continuous or limits failed, check the derivatives of the integral
            try:
                int_expr = sympy.integrate(witness, (t, z, z+h))
                right_deriv = sympy.limit(int_expr / h, h, 0, '+')
                left_deriv = sympy.limit(int_expr / h, h, 0, '-')
                
                if right_deriv != left_deriv or right_deriv != fz:
                    try:
                        diff1 = abs(float(right_deriv) - float(left_deriv))
                        diff2 = abs(float(right_deriv) - float(fz))
                        if diff1 > 1e-5 or diff2 > 1e-5:
                            neg_q = True
                            break
                    except Exception:
                        # If symbolic inequality holds but float conversion fails, trust symbolic
                        neg_q = True
                        break
            except Exception:
                # Fallback to numerical Riemann sum approximation
                try:
                    n_steps = 100
                    h_val = 1e-4
                    step = h_val / n_steps
                    
                    sum_right = 0
                    for i in range(n_steps):
                        sum_right += float(witness.subs(t, z + i*step + step/2).evalf()) * step
                    r_deriv = sum_right / h_val
                    
                    sum_left = 0
                    for i in range(n_steps):
                        sum_left += float(witness.subs(t, z - h_val + i*step + step/2).evalf()) * step
                    l_deriv = sum_left / h_val
                    
                    fz_val = float(fz.evalf())
                    
                    if abs(r_deriv - l_deriv) > 1e-3 or abs(r_deriv - fz_val) > 1e-3:
                        neg_q = True
                        break
                except Exception:
                    pass
                    
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is defined by F(x, y) = integral_x^y f(t) dt",
    "¬Q: F is NOT differentiable on R^2 with gradient (-f(x), f(y))"
]

N_HYP = 1
NEG_Q_INDEX = 1