import sympy
import math

# Top-level setup
x = sympy.Symbol('x', real=True)
n = sympy.Symbol('n', integer=True, positive=True)
k = sympy.Symbol('k', integer=True, positive=True)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: f is a 2*pi-periodic function
    h1_ok = False
    try:
        diff = sympy.simplify(witness.subs(x, x + 2*sympy.pi) - witness)
        if diff == 0:
            h1_ok = True
    except Exception:
        pass
        
    if not h1_ok:
        try:
            f_lam = sympy.lambdify(x, witness, modules=['math', 'sympy'])
            def f_func_per(t):
                return float(f_lam(t))
            f_func_per(0.1)
            
            is_per = True
            test_points = [-3.14, -1.5, -0.5, 0.0, 0.5, 1.5, 3.14, 2.718, -2.718, 1.234]
            for val in test_points:
                v1 = f_func_per(val)
                v2 = f_func_per(val + 2*math.pi)
                if abs(v1 - v2) > 1e-5 * (1 + abs(v1)):
                    is_per = False
                    break
            h1_ok = is_per
        except Exception:
            try:
                is_per = True
                test_points = [-3.14, -1.5, 0.0, 1.5, 3.14]
                for val in test_points:
                    v1 = float(witness.subs(x, val).evalf())
                    v2 = float(witness.subs(x, val + 2*sympy.pi).evalf())
                    if abs(v1 - v2) > 1e-5 * (1 + abs(v1)):
                        is_per = False
                        break
                h1_ok = is_per
            except Exception:
                h1_ok = False

    # neg_Q: The Fourier series of f does NOT converge absolutely
    neg_q = False
    
    # Shortcut for explicitly provided Fourier series (Sum objects)
    if witness.has(sympy.Sum):
        try:
            sums = witness.atoms(sympy.Sum)
            for s in sums:
                summand = s.args[0]
                var = s.args[1][0]
                
                # Extract amplitude by removing alternating signs and trig functions
                amp = summand.subs(sympy.S.NegativeOne**var, 1)
                amp = amp.replace(sympy.sin, lambda arg: sympy.S.One)
                amp = amp.replace(sympy.cos, lambda arg: sympy.S.One)
                amp = sympy.Abs(amp)
                
                # Check if the sum of amplitudes converges
                conv = sympy.Sum(amp, (var, 1, sympy.oo)).is_convergent()
                if conv == False:
                    return [h1_ok, True]
                elif conv == True:
                    return [h1_ok, False]
                
                # Fallback to limit check
                lim = sympy.limit(var * amp, var, sympy.oo)
                if lim.is_extended_real and lim > 0:
                    return [h1_ok, True]
            return [h1_ok, False]
        except Exception:
            pass

    # Numeric evaluation of Fourier coefficients decay rate
    try:
        try:
            f_lam = sympy.lambdify(x, witness, modules=['math', 'sympy'])
            def f_func_num(t):
                return float(f_lam(t))
            f_func_num(0.1)
        except Exception:
            def f_func_num(t):
                return float(witness.subs(x, t).evalf())
                
        def get_coeffs(n_val):
            N_steps = max(2000, n_val * 50)
            dt = 2 * math.pi / N_steps
            an_val = 0.0
            bn_val = 0.0
            for i in range(N_steps):
                t = -math.pi + (i + 0.5) * dt
                try:
                    val = f_func_num(t)
                except Exception:
                    val = 0.0
                an_val += val * math.cos(n_val * t)
                bn_val += val * math.sin(n_val * t)
            return an_val * dt / math.pi, bn_val * dt / math.pi

        n_vals = [10, 20, 40, 80, 160]
        C = []
        for n_val in n_vals:
            # Take max of n and n+1 to avoid zero coefficients due to symmetry
            an1, bn1 = get_coeffs(n_val)
            an2, bn2 = get_coeffs(n_val+1)
            C.append(max(abs(an1) + abs(bn1), abs(an2) + abs(bn2)))
            
        C40 = C[2]
        C160 = C[4]
        
        if C40 < 1e-7 and C160 < 1e-7:
            neg_q = False
        elif C40 > 1e-7 and C160 > 1e-7:
            # Estimate polynomial decay rate p (C_n ~ 1/n^p)
            p = -math.log(C160 / C40) / math.log(4.0)
            # If p <= 1.15, the sum of absolute values diverges
            if p <= 1.15:
                neg_q = True
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a 2*pi-periodic function",
    "¬Q: The Fourier series of f does not converge absolutely"
]

N_HYP = 1
NEG_Q_INDEX = 1