import sympy as sp
import itertools

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is d >= 2. For d = 1, the inequality fails.
    
    Expected witness format:
    {
        'd': int,
        'vars': list of sympy symbols (length d),
        'f_list': list of sympy expressions for f_i (length d),
        'f': sympy expression for f(x)
    }
    """
    try:
        d = int(witness['d'])
        vars = witness['vars']
        f_list = witness['f_list']
        f = witness['f']
    except Exception:
        return [False, False, False]
        
    if len(vars) != d or len(f_list) != d:
        return [False, False, False]

    def is_non_negative(expr, vs):
        if hasattr(expr, 'is_number') and expr.is_number:
            try:
                return float(expr) >= 0
            except Exception:
                return False
        # Check non-negativity at a few sample points
        for pts in itertools.product([-1.5, 0, 1.5], repeat=len(vs)):
            subs = dict(zip(vs, pts))
            try:
                val = float(expr.subs(subs) if hasattr(expr, 'subs') else expr)
                if val < 0:
                    return False
            except Exception:
                pass
        return True

    # H1: For each i, f_i is non-negative and in L^{d-1}(R^{d-1})
    h1 = True
    norms = []
    try:
        for i in range(d):
            fi = f_list[i]
            fi_vars = [vars[j] for j in range(d) if j != i]
            
            if not is_non_negative(fi, fi_vars):
                h1 = False
                break
                
            if d == 1:
                # For d=1, L^0 norm on R^0 (a point) is just the absolute value of the constant
                val = float(fi)
                norms.append(val)
            else:
                integrand = fi**(d-1)
                for v in fi_vars:
                    integrand = sp.integrate(integrand, (v, -sp.oo, sp.oo))
                
                if integrand == sp.oo or integrand.has(sp.nan):
                    h1 = False
                    norms.append(sp.oo)
                else:
                    norm = integrand**sp.Rational(1, d-1)
                    norms.append(norm)
    except Exception:
        h1 = False

    # H2: f(x) = prod f_i
    h2 = False
    try:
        prod = 1
        for fi in f_list:
            prod *= fi
        
        if hasattr(f, 'equals'):
            if f.equals(prod):
                h2 = True
            else:
                diff = sp.simplify(f - prod)
                if diff == 0:
                    h2 = True
        else:
            diff = sp.simplify(f - prod)
            if diff == 0:
                h2 = True
    except Exception:
        h2 = False

    # Conclusion: int f <= prod norms
    neg_q = False
    try:
        lhs = f
        for v in vars:
            lhs = sp.integrate(lhs, (v, -sp.oo, sp.oo))
        
        rhs = 1
        for n in norms:
            rhs *= n
            
        if lhs == sp.oo and rhs != sp.oo:
            neg_q = True
        elif lhs != sp.oo and rhs == sp.oo:
            neg_q = False
        elif lhs == sp.oo and rhs == sp.oo:
            neg_q = False
        else:
            diff = sp.simplify(lhs - rhs)
            try:
                if bool(diff > 0):
                    neg_q = True
            except TypeError:
                if diff.evalf() > 0:
                    neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    r"H_1: For each 1 <= i <= d, f_i is a non-negative measurable function in L^{d-1}(R^{d-1})",
    r"H_2: f(x) = prod_{i=1}^d f_i(x_1, ..., \hat{x_i}, ..., x_d) for almost all x in R^d",
    r"not Q: int_{R^d} f(x) dx > prod_{i=1}^d ||f_i||_{L^{d-1}(R^{d-1})}"
]

N_HYP = 2
NEG_Q_INDEX = 2