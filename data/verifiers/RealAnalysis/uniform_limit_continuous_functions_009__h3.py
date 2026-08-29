import sympy

# Top-level setup
x = sympy.Symbol('x')
n = sympy.Symbol('n', integer=True, positive=True)

def get_test_points(domain, p):
    points = [p]
    try:
        if hasattr(domain, 'inf') and domain.inf.is_finite:
            if domain.contains(domain.inf) == True and domain.inf not in points:
                points.append(domain.inf)
    except Exception:
        pass
    try:
        if hasattr(domain, 'sup') and domain.sup.is_finite:
            if domain.contains(domain.sup) == True and domain.sup not in points:
                points.append(domain.sup)
    except Exception:
        pass
    try:
        if hasattr(domain, 'inf') and hasattr(domain, 'sup') and domain.inf.is_finite and domain.sup.is_finite:
            mid = (domain.inf + domain.sup) / 2
            if domain.contains(mid) == True and mid not in points:
                points.append(mid)
        else:
            for val in [0, 1, -1]:
                if domain.contains(sympy.S(val)) == True and val not in points:
                    points.append(sympy.S(val))
    except Exception:
        pass
    return points

def conditions(witness):
    """
    witness can be either:
      (f_n, f, domain, x_sym, n_sym, p)
      (f_n, domain, x_sym, n_sym, p)
    where:
      f_n: SymPy expression for the sequence of functions
      f: SymPy expression for the limit function (optional, will be computed if omitted)
      domain: SymPy Set representing the domain A
      x_sym: SymPy Symbol for the variable
      n_sym: SymPy Symbol for the sequence index
      p: A point in A where the limit function f is discontinuous
    """
    try:
        if len(witness) == 6:
            f_n, f, domain, x_sym, n_sym, p = witness
        elif len(witness) == 5:
            f_n, domain, x_sym, n_sym, p = witness
            f = sympy.limit(f_n, n_sym, sympy.oo)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: (f_n) is a sequence of real-valued functions defined on A
    h1_ok = True
    try:
        if not domain.is_subset(sympy.S.Reals):
            h1_ok = False
        
        if domain.contains(p) != True:
            h1_ok = False
            
        test_points = get_test_points(domain, p)
        for q in test_points:
            for k in [1, 2, 3]:
                val = f_n.subs({n_sym: k, x_sym: q})
                if val.is_real == False or val in [sympy.oo, -sympy.oo, sympy.zoo]:
                    h1_ok = False
                if sympy.im(val) != 0:
                    h1_ok = False
            
            lim_val = sympy.limit(f_n.subs(x_sym, q), n_sym, sympy.oo)
            if lim_val.is_real == False or lim_val in [sympy.oo, -sympy.oo, sympy.zoo]:
                h1_ok = False
                
            f_q = f.subs(x_sym, q)
            diff = lim_val - f_q
            if diff != 0 and sympy.simplify(diff) != 0:
                h1_ok = False
    except Exception:
        h1_ok = False

    # H2: Each function f_n is continuous on A
    h2_ok = True
    try:
        test_points = get_test_points(domain, p)
        for q in test_points:
            for k in [1, 2, 3]:
                fn_k = f_n.subs(n_sym, k)
                val = fn_k.subs(x_sym, q)
                
                if not (hasattr(domain, 'sup') and q == domain.sup):
                    lim_right = sympy.limit(fn_k, x_sym, q, dir='+')
                    diff = lim_right - val
                    if diff != 0 and sympy.simplify(diff) != 0:
                        h2_ok = False
                
                if not (hasattr(domain, 'inf') and q == domain.inf):
                    lim_left = sympy.limit(fn_k, x_sym, q, dir='-')
                    diff = lim_left - val
                    if diff != 0 and sympy.simplify(diff) != 0:
                        h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The limit function f is not continuous on A
    neg_q_ok = False
    try:
        f_val = f.subs(x_sym, p)
        
        if not (hasattr(domain, 'sup') and p == domain.sup):
            lim_right = sympy.limit(f, x_sym, p, dir='+')
            diff = lim_right - f_val
            if diff != 0 and sympy.simplify(diff) != 0:
                neg_q_ok = True
                
        if not (hasattr(domain, 'inf') and p == domain.inf):
            lim_left = sympy.limit(f, x_sym, p, dir='-')
            diff = lim_left - f_val
            if diff != 0 and sympy.simplify(diff) != 0:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of real-valued functions defined on A",
    "H_2: Each function f_n is continuous on A",
    "¬Q: The limit function f is not continuous on A"
]

N_HYP = 2
NEG_Q_INDEX = 2