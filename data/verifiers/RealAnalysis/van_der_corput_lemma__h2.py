import sympy
import math

# Top-level setup
x, y, z, t = sympy.symbols('x y z t')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            phi = sympy.sympify(witness['phi'])
            a = sympy.sympify(witness['a'])
            b = sympy.sympify(witness['b'])
            lambda_ = sympy.sympify(witness['lambda'])
            var = witness.get('x')
        else:
            if len(witness) == 5:
                phi, a, b, lambda_, var = witness
                phi = sympy.sympify(phi)
                a = sympy.sympify(a)
                b = sympy.sympify(b)
                lambda_ = sympy.sympify(lambda_)
            elif len(witness) == 4:
                phi, a, b, lambda_ = witness
                phi = sympy.sympify(phi)
                a = sympy.sympify(a)
                b = sympy.sympify(b)
                lambda_ = sympy.sympify(lambda_)
                var = None
            else:
                return [False, False, False]
                
        if var is None:
            free = phi.free_symbols
            if len(free) == 1:
                var = list(free)[0]
            elif len(free) == 0:
                var = x
            else:
                return [False, False, False]
        else:
            var = sympy.sympify(var)
            
        a_f = float(a)
        b_f = float(b)
        lam_f = float(lambda_)
    except Exception:
        return [False, False, False]

    # H1: phi is continuously differentiable on the interval
    try:
        h1_ok = False
        if a_f < b_f:
            phi_prime = sympy.diff(phi, var)
            f_prime = sympy.lambdify(var, phi_prime, 'math')
            n_points = 100
            h1_ok = True
            for i in range(n_points + 1):
                val = f_prime(a_f + (b_f - a_f) * i / n_points)
                if math.isnan(val) or math.isinf(val):
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H2: |phi'(x)| >= lambda > 0 for all x in the interval
    try:
        h2_ok = False
        if lam_f > 0:
            phi_prime = sympy.diff(phi, var)
            f_prime = sympy.lambdify(var, phi_prime, 'math')
            n_points = 1000
            h2_ok = True
            for i in range(n_points + 1):
                val = f_prime(a_f + (b_f - a_f) * i / n_points)
                if abs(val) < lam_f - 1e-7:
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False

    # ¬Q: |int_a^b e^{i phi(x)} dx| > 3 / lambda
    try:
        neg_q_ok = False
        f = sympy.lambdify(var, phi, 'math')
        n = 100000
        h = (b_f - a_f) / n
        
        sum_odd = 0j
        sum_even = 0j
        
        for i in range(1, n, 2):
            pt = f(a_f + i * h)
            sum_odd += complex(math.cos(pt), math.sin(pt))
            
        for i in range(2, n, 2):
            pt = f(a_f + i * h)
            sum_even += complex(math.cos(pt), math.sin(pt))
            
        pt_a = f(a_f)
        pt_b = f(b_f)
        integral = (complex(math.cos(pt_a), math.sin(pt_a)) + 
                    complex(math.cos(pt_b), math.sin(pt_b)) + 
                    4 * sum_odd + 2 * sum_even) * (h / 3)
                    
        if abs(integral) > 3.0 / lam_f + 1e-7:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi is continuously differentiable",
    "H_2: derivative of phi is bounded below by lambda",
    "¬Q: integral bound fails"
]

N_HYP = 2
NEG_Q_INDEX = 2