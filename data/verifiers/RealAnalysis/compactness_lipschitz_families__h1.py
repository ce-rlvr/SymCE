import sympy as sp
import itertools
import math

# Top-level setup for witness expressions
x, n = sp.symbols('x n', real=True)

def conditions(witness):
    try:
        f_input = witness.get('f')
        M = float(witness.get('M', 0))
        L = float(witness.get('L', 0))
        c = float(witness.get('c', 0))
        
        # Wrap the function to ensure it evaluates to a real float
        if isinstance(f_input, sp.Expr):
            n_sym = witness.get('n', sp.Symbol('n'))
            x_sym = witness.get('x', sp.Symbol('x'))
            modules = [{'Max': max, 'Min': min, 'Abs': abs}, 'math', 'sympy']
            f_lambdified = sp.lambdify((n_sym, x_sym), f_input, modules=modules)
            
            def f(n_val, x_val):
                res = f_lambdified(n_val, x_val)
                if isinstance(res, sp.Expr):
                    res = complex(res.evalf())
                else:
                    res = complex(res)
                if abs(res.imag) > 1e-9:
                    raise ValueError("Non-real value")
                return float(res.real)
        else:
            def f(n_val, x_val):
                res = f_input(n_val, x_val)
                if isinstance(res, sp.Expr):
                    res = complex(res.evalf())
                else:
                    res = complex(res)
                if abs(res.imag) > 1e-9:
                    raise ValueError("Non-real value")
                return float(res.real)

        # Setup test indices (n)
        test_n_raw = witness.get('test_n')
        if test_n_raw is None:
            test_n = list(range(1, 21))
        else:
            test_n = []
            for val in test_n_raw[:50]:
                try:
                    int_val = int(val)
                    if int_val not in test_n:
                        test_n.append(int_val)
                except Exception:
                    pass
            if len(test_n) < 2:
                test_n = list(range(1, 21))

        # Setup test domain points (x)
        test_x_raw = witness.get('test_x', [])
        test_x_custom = []
        for val in test_x_raw[:1000]:
            try:
                test_x_custom.append(float(val))
            except Exception:
                pass
                
        default_x = [i * 0.5 for i in range(-200, 201)] + [i * 10.0 for i in range(-200, 201)]
        test_x = sorted(list(set(test_x_custom + default_x)))

        # Apply optional domain filter
        domain_filter = witness.get('domain_filter')
        if domain_filter is not None:
            filtered_x = []
            for x_val in test_x:
                try:
                    if domain_filter(x_val):
                        filtered_x.append(x_val)
                except Exception:
                    pass
            test_x = filtered_x

        if len(test_x) < 2 or len(test_n) < 2:
            return [False, False, False, False]

        # H1: F is a family of real-valued functions on K
        h1 = True
        for n_val in test_n[:5]:
            for x_val in test_x[:10]:
                try:
                    val = f(n_val, x_val)
                    if math.isnan(val) or math.isinf(val):
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break
            if not h1: break

        # H2: Uniformly bounded by M
        h2 = True
        if M <= 0:
            h2 = False
        else:
            for n_val in test_n:
                for x_val in test_x:
                    try:
                        if abs(f(n_val, x_val)) > M + 1e-4:
                            h2 = False
                            break
                    except Exception:
                        h2 = False
                        break
                if not h2: break

        # H3: Uniformly Lipschitz with constant L
        h3 = True
        if L <= 0:
            h3 = False
        else:
            # 1. Check adjacent points for steep gradients
            for n_val in test_n[:10]:
                for i in range(len(test_x) - 1):
                    x_val = test_x[i]
                    y_val = test_x[i+1]
                    if abs(x_val - y_val) > 1e-9:
                        try:
                            if abs(f(n_val, x_val) - f(n_val, y_val)) > L * abs(x_val - y_val) + 1e-4:
                                h3 = False
                                break
                        except Exception:
                            h3 = False
                            break
                if not h3: break
            
            # 2. Check all pairs in a subset for global Lipschitz compliance
            if h3:
                subset_x = test_x[::max(1, len(test_x)//50)]
                for n_val in test_n[:5]:
                    for i in range(len(subset_x)):
                        for j in range(i + 1, len(subset_x)):
                            x_val = subset_x[i]
                            y_val = subset_x[j]
                            if abs(x_val - y_val) > 1e-9:
                                try:
                                    if abs(f(n_val, x_val) - f(n_val, y_val)) > L * abs(x_val - y_val) + 1e-4:
                                        h3 = False
                                        break
                                except Exception:
                                    h3 = False
                                    break
                        if not h3: break
                    if not h3: break

        # Negated Conclusion: No uniformly convergent subsequence
        # (Verified by checking if the sequence is uniformly separated by c > 0)
        neg_q = True
        if c <= 0:
            neg_q = False
        else:
            for n_val, m_val in itertools.combinations(test_n, 2):
                max_diff = 0
                for x_val in test_x:
                    try:
                        diff = abs(f(n_val, x_val) - f(m_val, x_val))
                        if diff > max_diff:
                            max_diff = diff
                    except Exception:
                        pass
                if max_diff < c - 1e-4:
                    neg_q = False
                    break

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a family of real-valued functions on K",
    "H_2: F is uniformly bounded by M",
    "H_3: F is uniformly Lipschitz with constant L",
    "¬Q: F has a sequence with no uniformly convergent subsequence"
]

N_HYP = 3
NEG_Q_INDEX = 3