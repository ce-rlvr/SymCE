import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is a mu-integrable function",
    "H_2: phi is a convex function",
    "H_3: phi o f is mu-integrable",
    "¬Q: phi(int f dmu) > int phi o f dmu"
]
N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        h1 = h2 = h3 = neg_q = False
        
        # Parse witness
        is_discrete = False
        if isinstance(witness, dict):
            if 'domain' in witness:
                f = witness['f']
                phi = witness['phi']
                mu = witness.get('mu', 1)
                domain = witness['domain']
                is_discrete = False
            elif 'f' in witness and isinstance(witness['f'], (list, tuple)):
                f = witness['f']
                phi = witness['phi']
                mu = witness.get('mu', [1]*len(f))
                is_discrete = True
            else:
                return [False, False, False, False]
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                f, phi, domain, mu = witness
                is_discrete = False
            elif len(witness) == 3:
                f, phi, third = witness
                if isinstance(f, (list, tuple)):
                    mu = third
                    is_discrete = True
                else:
                    domain = third
                    mu = 1
                    is_discrete = False
            elif len(witness) == 2:
                f, phi = witness
                if isinstance(f, (list, tuple)):
                    mu = [1]*len(f)
                    is_discrete = True
                else:
                    return [False, False, False, False]
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]

        # Process phi
        x_sym = sp.Symbol('x', real=True)
        if callable(phi):
            try:
                phi_expr = phi(x_sym)
            except Exception:
                return [False, False, False, False]
        elif isinstance(phi, (int, float)):
            phi_expr = sp.S(phi)
        elif hasattr(phi, 'free_symbols'):
            free_syms = phi.free_symbols
            if len(free_syms) == 1:
                sym = list(free_syms)[0]
                phi_expr = phi.subs(sym, x_sym)
            elif len(free_syms) == 0:
                phi_expr = phi
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]

        # Check H2: phi is convex
        if phi_expr == sp.Abs(x_sym):
            h2 = True
        else:
            d2phi = sp.diff(phi_expr, x_sym, 2)
            if d2phi.is_constant():
                h2 = bool(d2phi >= 0)
            else:
                try:
                    neg_set = sp.solveset(d2phi < 0, x_sym, domain=sp.S.Reals)
                    if neg_set == sp.S.EmptySet:
                        h2 = True
                    else:
                        if isinstance(neg_set, sp.ConditionSet):
                            raise ValueError
                        h2 = False
                except Exception:
                    try:
                        # Deterministic numerical fallback for convexity
                        is_convex = True
                        pts = [i * 1.0 for i in range(-10, 11)]
                        for x1 in pts:
                            for x2 in pts:
                                val_mid = phi_expr.subs(x_sym, 0.5*x1 + 0.5*x2)
                                val_comb = 0.5*phi_expr.subs(x_sym, x1) + 0.5*phi_expr.subs(x_sym, x2)
                                if float(val_mid) > float(val_comb) + 1e-7:
                                    is_convex = False
                                    break
                            if not is_convex:
                                break
                        h2 = is_convex
                    except Exception:
                        h2 = False

        if is_discrete:
            # Check if mu is a valid positive measure
            if not all(float(m) >= -1e-9 for m in mu):
                return [False, False, False, False]
            
            # Finite discrete sums are always integrable
            h1 = True
            h3 = True
            
            try:
                int_f = sum(f_val * mu_val for f_val, mu_val in zip(f, mu))
                lhs = phi_expr.subs(x_sym, int_f)
                
                int_phi_f = sum(phi_expr.subs(x_sym, f_val) * mu_val for f_val, mu_val in zip(f, mu))
                rhs = int_phi_f
                
                diff = sp.simplify(lhs - rhs)
                if diff.is_positive:
                    neg_q = True
                elif diff.is_negative or diff.is_zero:
                    neg_q = False
                else:
                    neg_q = bool(float(lhs) > float(rhs) + 1e-9)
            except Exception:
                neg_q = False
                
        else:
            a, b = domain
            
            # Process f
            if callable(f):
                f_expr = f(x_sym)
            elif isinstance(f, (int, float)):
                f_expr = sp.S(f)
            elif hasattr(f, 'free_symbols'):
                f_syms = f.free_symbols
                if len(f_syms) == 1:
                    f_expr = f.subs(list(f_syms)[0], x_sym)
                elif len(f_syms) == 0:
                    f_expr = f
                else:
                    return [False, False, False, False]
            else:
                f_expr = sp.S(f)
                
            # Process mu
            if callable(mu):
                mu_expr = mu(x_sym)
            elif isinstance(mu, (int, float)):
                mu_expr = sp.S(mu)
            elif hasattr(mu, 'free_symbols'):
                mu_syms = mu.free_symbols
                if len(mu_syms) == 1:
                    mu_expr = mu.subs(list(mu_syms)[0], x_sym)
                elif len(mu_syms) == 0:
                    mu_expr = mu
                else:
                    return [False, False, False, False]
            else:
                mu_expr = sp.S(mu)

            # Check if mu is a valid positive measure
            try:
                test_pts = []
                if a == -sp.oo and b == sp.oo:
                    test_pts = [-10, -1, 0, 1, 10]
                elif a == -sp.oo:
                    test_pts = [b-10, b-1, b]
                elif b == sp.oo:
                    test_pts = [a, a+1, a+10]
                else:
                    test_pts = [a + (b-a)*i/10.0 for i in range(1, 10)]
                
                vals = [mu_expr.subs(x_sym, pt) for pt in test_pts]
                if not all(float(v) >= -1e-9 for v in vals):
                    return [False, False, False, False]
            except Exception:
                pass

            # Check H1: f is mu-integrable
            try:
                int_abs_f = sp.integrate(sp.Abs(f_expr) * mu_expr, (x_sym, a, b))
                if int_abs_f.has(sp.Integral):
                    int_abs_f = int_abs_f.evalf()
                h1 = True
                float(int_abs_f)  # Raises TypeError if not a finite real number
            except Exception:
                h1 = False
                
            # Check H3: phi(f) is mu-integrable
            try:
                phi_f = phi_expr.subs(x_sym, f_expr)
                int_abs_phi_f = sp.integrate(sp.Abs(phi_f) * mu_expr, (x_sym, a, b))
                if int_abs_phi_f.has(sp.Integral):
                    int_abs_phi_f = int_abs_phi_f.evalf()
                h3 = True
                float(int_abs_phi_f)
            except Exception:
                h3 = False
                
            # Check Conclusion
            try:
                int_f = sp.integrate(f_expr * mu_expr, (x_sym, a, b))
                int_phi_f = sp.integrate(phi_f * mu_expr, (x_sym, a, b))
                
                lhs = phi_expr.subs(x_sym, int_f)
                rhs = int_phi_f
                
                diff = sp.simplify(lhs - rhs)
                if diff.is_positive:
                    neg_q = True
                elif diff.is_negative or diff.is_zero:
                    neg_q = False
                else:
                    neg_q = bool(float(lhs.evalf()) > float(rhs.evalf()) + 1e-9)
            except Exception:
                neg_q = False

        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]