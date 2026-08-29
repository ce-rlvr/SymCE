import sympy
from sympy import Interval, Union, FiniteSet, Reals, Symbol, solveset, integrate, oo

# Top-level setup
x = Symbol('x')

def eval_f(f, x_sym, val):
    if hasattr(f, 'subs'):
        return f.subs(x_sym, val)
    return f

def eval_density(density, x_sym, val):
    if hasattr(density, 'subs'):
        return density.subs(x_sym, val)
    return density

def compute_integral(expr, x_sym, domain, density=1):
    integrand = expr * density
    if isinstance(domain, FiniteSet):
        return sum(eval_f(integrand, x_sym, val) for val in domain.args)
    elif isinstance(domain, Union):
        return sum(compute_integral(expr, x_sym, arg, density) for arg in domain.args)
    elif isinstance(domain, Interval):
        return integrate(integrand, (x_sym, domain.start, domain.end))
    else:
        try:
            return integrate(integrand, (x_sym, domain))
        except Exception:
            if domain == Reals:
                return integrate(integrand, (x_sym, -oo, oo))
            raise

def get_witness_elements(witness):
    if isinstance(witness, dict):
        f = witness['f']
        x_sym = witness.get('x')
        if x_sym is None:
            if hasattr(f, 'free_symbols') and f.free_symbols:
                x_sym = list(f.free_symbols)[0]
            else:
                x_sym = Symbol('x')
        if callable(f):
            f = f(x_sym)
        t = witness['t']
        domain = witness.get('domain', Reals)
        density = witness.get('density', 1)
        return f, x_sym, t, domain, density
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            f, t = witness
            x_sym = list(f.free_symbols)[0] if hasattr(f, 'free_symbols') and f.free_symbols else Symbol('x')
            if callable(f):
                f = f(x_sym)
            return f, x_sym, t, Reals, 1
        elif len(witness) == 3:
            if isinstance(witness[1], (int, float, sympy.Expr)) and not isinstance(witness[1], sympy.Set):
                f, t, domain = witness
            else:
                f, domain, t = witness
            x_sym = list(f.free_symbols)[0] if hasattr(f, 'free_symbols') and f.free_symbols else Symbol('x')
            if callable(f):
                f = f(x_sym)
            return f, x_sym, t, domain, 1
        elif len(witness) == 4:
            f, x_sym, t, domain = witness
            if callable(f):
                f = f(x_sym)
            return f, x_sym, t, domain, 1
        elif len(witness) == 5:
            f, x_sym, t, domain, density = witness
            if callable(f):
                f = f(x_sym)
            return f, x_sym, t, domain, density
    return None

def conditions(witness) -> list[bool]:
    # Check for discrete dict-based witness (e.g., finite signed measure space)
    if isinstance(witness, dict) and isinstance(witness.get('f'), dict):
        try:
            f_dict = witness['f']
            probs = witness.get('probs', witness.get('mu', witness.get('measure', witness.get('density', {k: 1 for k in f_dict}))))
            t = witness['t']
            
            h1_ok = all(v >= 0 for v in f_dict.values())
            h2_ok = bool(t > 0)
            
            meas = sum(probs.get(k, 1) for k, v in f_dict.items() if v >= t)
            integral_val = sum(probs.get(k, 1) * v for k, v in f_dict.items())
            
            neg_q = bool(meas > integral_val / t)
            return [h1_ok, h2_ok, neg_q]
        except Exception:
            pass

    # Otherwise, assume sympy-based witness
    try:
        elements = get_witness_elements(witness)
        if elements is None:
            return [False, False, False]
        f, x_sym, t, domain, density = elements
    except Exception:
        return [False, False, False]

    # H1: f is a non-negative measurable function on X
    try:
        if isinstance(domain, FiniteSet):
            h1_ok = all(eval_f(f, x_sym, val) >= 0 for val in domain.args)
        else:
            neg_set = solveset(f < 0, x_sym, domain=domain)
            h1_ok = bool(neg_set.is_empty)
    except Exception:
        h1_ok = False

    # H2: t > 0 is a real number
    try:
        h2_ok = bool(t > 0)
    except Exception:
        h2_ok = False

    # neg_Q: \mu(\{x \in X : f(x) \ge t\}) > \frac{1}{t} \int_X f \, d\mu
    try:
        if isinstance(domain, FiniteSet):
            meas = sum(eval_density(density, x_sym, val) for val in domain.args if eval_f(f, x_sym, val) >= t)
            integral_val = sum(eval_f(f, x_sym, val) * eval_density(density, x_sym, val) for val in domain.args)
        else:
            sol_set = solveset(f >= t, x_sym, domain=domain)
            if density == 1:
                meas = sol_set.measure
            else:
                meas = compute_integral(1, x_sym, sol_set, density)
            integral_val = compute_integral(f, x_sym, domain, density)
            
        meas_sym = sympy.sympify(meas).evalf()
        int_sym = sympy.sympify(integral_val).evalf()
        t_sym = sympy.sympify(t).evalf()
        
        try:
            meas_f = float(meas_sym)
            int_f = float(int_sym)
            t_f = float(t_sym)
            neg_q = meas_f > int_f / t_f
        except TypeError:
            neg_q = bool(meas_sym > int_sym / t_sym)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a non-negative measurable function on X",
    "H_2: t > 0 is a real number",
    "¬Q: \mu(\{x \in X : f(x) \ge t\}) > \frac{1}{t} \int_X f \, d\mu"
]

N_HYP = 2
NEG_Q_INDEX = 2