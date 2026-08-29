import sympy as sp
import math

# Top-level setup for convenience
x, n = sp.symbols('x n')

CONDITION_LABELS = [
    "H_1: (\\Omega, \\Sigma, \\mu) is a measure space",
    "H_2: (f_n) is a sequence of measurable functions",
    "H_3: \\limsup_{n \\to \\infty} f_n is measurable",
    "¬Q: \\limsup_{n \\to \\infty} \\int_{\\Omega} f_n d\\mu > \\int_{\\Omega} \\limsup_{n \\to \\infty} f_n d\\mu"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false Reverse Fatou's Lemma.
    The witness should be a dictionary providing the sequence of functions and their limits/integrals.
    """
    def eval_expr(expr, subs_dict):
        if isinstance(expr, (int, float)):
            return float(expr)
        if hasattr(expr, 'subs'):
            val = expr.subs(subs_dict).evalf()
            return float(val)
        return float(expr)

    def check_close(val, expected):
        try:
            val = float(val)
            expected = float(expected)
        except Exception:
            return False
            
        if math.isinf(expected):
            if math.isinf(val) and val == expected:
                return True
            if expected > 0 and val > 100:
                return True
            if expected < 0 and val < -100:
                return True
            return False
            
        if math.isnan(expected):
            return math.isnan(val)
            
        return abs(val - expected) <= 1e-3

    try:
        f_n = witness['f_n']
        n_sym = witness.get('n', n)
        x_sym = witness.get('x', x)
        domain = witness.get('domain', 'N')
        limsup_f_n = witness['limsup_f_n']
        int_f_n = witness['int_f_n']
        limsup_int_f_n = float(witness['limsup_int_f_n'])
        int_limsup = float(witness['int_limsup'])
        
        # H1: Measure space
        h1 = domain in ['N', 'R']
        
        # H2: f_n is a sequence of measurable functions
        h2 = True
        try:
            eval_expr(f_n, {n_sym: 1, x_sym: 1})
        except Exception:
            h2 = False
            
        int_fn_ok = True
        if domain == 'N':
            for n_val in [1, 2, 3]:
                total = sum(eval_expr(f_n, {n_sym: n_val, x_sym: x_val}) for x_val in range(1, 201))
                expected = eval_expr(int_f_n, {n_sym: n_val})
                if not check_close(total, expected):
                    int_fn_ok = False
                    break
        elif domain == 'R':
            for n_val in [1, 2]:
                fn_sub = f_n.subs(n_sym, n_val) if hasattr(f_n, 'subs') else f_n
                val = sp.integrate(fn_sub, (x_sym, -sp.oo, sp.oo))
                expected = eval_expr(int_f_n, {n_sym: n_val})
                if not check_close(val, expected):
                    int_fn_ok = False
                    break
                    
        h2 = h2 and int_fn_ok
        
        # H3: limsup f_n is measurable
        h3 = True
        try:
            eval_expr(limsup_f_n, {x_sym: 1})
        except Exception:
            h3 = False
            
        limsup_fn_ok = True
        for x_val in [1, 2, 3]:
            expected = eval_expr(limsup_f_n, {x_sym: x_val})
            try:
                sym_limit = sp.limit(f_n.subs(x_sym, x_val) if hasattr(f_n, 'subs') else f_n, n_sym, sp.oo)
                if not check_close(sym_limit.evalf(), expected):
                    raise ValueError("Limit mismatch, fallback to numerical")
            except Exception:
                vals = []
                for n_val in range(100, 150):
                    v = eval_expr(f_n, {n_sym: n_val, x_sym: x_val})
                    vals.append(v)
                approx_limsup = max(vals)
                val_150 = eval_expr(f_n, {n_sym: 150, x_sym: x_val})
                if not (check_close(approx_limsup, expected) or check_close(val_150, expected)):
                    limsup_fn_ok = False
                    break
                
        int_limsup_ok = True
        if domain == 'N':
            total = sum(eval_expr(limsup_f_n, {x_sym: x_val}) for x_val in range(1, 201))
            if not check_close(total, int_limsup):
                int_limsup_ok = False
        elif domain == 'R':
            val = sp.integrate(limsup_f_n, (x_sym, -sp.oo, sp.oo))
            if not check_close(val, int_limsup):
                int_limsup_ok = False
                
        limsup_int_fn_ok = True
        try:
            sym_limit = sp.limit(int_f_n, n_sym, sp.oo)
            if not check_close(sym_limit.evalf(), limsup_int_f_n):
                raise ValueError("Limit mismatch, fallback to numerical")
        except Exception:
            vals = []
            for n_val in range(100, 150):
                v = eval_expr(int_f_n, {n_sym: n_val})
                vals.append(v)
            approx_limsup_int = max(vals)
            val_150 = eval_expr(int_f_n, {n_sym: 150})
            if not (check_close(approx_limsup_int, limsup_int_f_n) or check_close(val_150, limsup_int_f_n)):
                limsup_int_fn_ok = False
            
        h3 = h3 and limsup_fn_ok and int_limsup_ok and limsup_int_fn_ok
        
        # Negated conclusion: limsup int f_n > int limsup f_n
        neg_q = limsup_int_f_n > int_limsup
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]