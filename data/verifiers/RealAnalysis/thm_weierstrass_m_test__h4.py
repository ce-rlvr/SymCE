from sympy import *
from sympy.abc import x, n

# Top-level setup
# The witness should be a tuple (D, f, M) where:
# - D is a SymPy Set (e.g., Reals, Interval(0, 1))
# - f is a SymPy Expr representing f_n(x) in terms of x and n
# - M is a SymPy Expr representing M_n in terms of n

def conditions(witness) -> list[bool]:
    try:
        D, f, M = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: D is a set
    try:
        h1 = isinstance(D, Set)
    except Exception:
        h1 = False

    # H2: f_n is a sequence of functions from D to reals
    try:
        h2 = isinstance(f, Expr) and f.free_symbols.issubset({x, n})
    except Exception:
        h2 = False

    # H3: M_n is a sequence of non-negative reals
    try:
        h3 = isinstance(M, Expr) and M.free_symbols.issubset({n})
        if h3:
            for i in range(1, 20):
                val = M.subs(n, i).evalf()
                if val < 0:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # H4: The series \sum_{n=1}^\infty M_n converges
    try:
        h4 = False
        conv = Sum(M, (n, 1, oo)).is_convergent()
        if conv is S.true:
            h4 = True
        else:
            val = Sum(M, (n, 1, oo)).doit()
            if val.is_finite:
                h4 = True
    except Exception:
        h4 = False

    # Negated Conclusion: The series \sum_{n=1}^\infty f_n(x) does NOT converge uniformly and absolutely on D
    neg_q = False
    try:
        test_points = [S(0), S(1), S(-1), S(2), S(-2), S.Half, -S.Half, S(10), S(-10), S.Pi, S.Pi/2, S.Pi/4, S.Exp1]
        if hasattr(D, 'inf') and D.inf.is_finite: test_points.append(D.inf)
        if hasattr(D, 'sup') and D.sup.is_finite: test_points.append(D.sup)
        if hasattr(D, 'inf') and hasattr(D, 'sup') and D.inf.is_finite and D.sup.is_finite:
            test_points.append((D.inf + D.sup)/2)
            test_points.append(D.inf + (D.sup - D.inf)/4)
            test_points.append(D.sup - (D.sup - D.inf)/4)
            
        if hasattr(D, 'args'):
            for arg in D.args:
                if hasattr(arg, 'is_finite') and arg.is_finite:
                    test_points.append(arg)
                    
        valid_points = []
        for p in test_points:
            try:
                if D.contains(p) is S.true and p not in valid_points:
                    valid_points.append(p)
            except Exception:
                pass
                
        for p in valid_points:
            term = f.subs(x, p)
            
            # 1. Limit of terms is not zero
            L = limit(term, n, oo)
            if isinstance(L, Limit):
                val = term.subs(n, 1000).evalf()
                if val.is_real and abs(val) > 1:
                    neg_q = True
                    break
            elif L != 0:
                neg_q = True
                break
                
            # 2. Sum of absolute values diverges
            if Sum(Abs(term), (n, 1, oo)).is_convergent() is S.false:
                neg_q = True
                break
                
            # 3. Sum diverges
            if Sum(term, (n, 1, oo)).is_convergent() is S.false:
                neg_q = True
                break
                
        # 4. Check for lack of uniform convergence via sequences x_n
        if not neg_q:
            test_seqs = [n, n**2, 2**n, 1/n, 1/n**2, 1/sqrt(n), exp(n), log(n)]
            if hasattr(D, 'sup') and D.sup.is_finite:
                test_seqs.extend([D.sup - 1/n, D.sup - 1/n**2, D.sup - 1/sqrt(n)])
            if hasattr(D, 'inf') and D.inf.is_finite:
                test_seqs.extend([D.inf + 1/n, D.inf + 1/n**2, D.inf + 1/sqrt(n)])
                
            for seq in test_seqs:
                try:
                    in_D = True
                    for test_n in [10, 100]:
                        val = seq.subs(n, test_n).evalf()
                        if D.contains(val) is S.false:
                            in_D = False
                            break
                    if in_D:
                        term_seq = f.subs(x, seq)
                        L_seq = limit(term_seq, n, oo)
                        if isinstance(L_seq, Limit):
                            val = term_seq.subs(n, 1000).evalf()
                            if val.is_real and abs(val) > 1:
                                neg_q = True
                                break
                        elif L_seq != 0:
                            neg_q = True
                            break
                except Exception:
                    pass

        # 5. Check for lack of uniform convergence via discontinuity of the limit function
        if not neg_q and isinstance(D, Interval):
            try:
                S_inf = Sum(f, (n, 1, oo)).doit()
                if isinstance(S_inf, Expr) and not S_inf.has(Sum):
                    for p in [D.inf, D.sup]:
                        if p.is_finite and D.contains(p) is S.true:
                            sum_at_p = Sum(f.subs(x, p), (n, 1, oo)).doit()
                            lim_at_p = limit(S_inf, x, p, dir='-' if p == D.sup else '+')
                            if sum_at_p != lim_at_p:
                                neg_q = True
                                break
            except Exception:
                pass

    except Exception:
        pass

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: D is a set",
    "H_2: (f_n) is a sequence of functions from D to the real numbers",
    "H_3: (M_n) is a sequence of non-negative real numbers",
    "H_4: The series \\sum_{n=1}^\\infty M_n converges",
    "¬Q: The series \\sum_{n=1}^\\infty f_n(x) does not converge uniformly and absolutely on D"
]

N_HYP = 4
NEG_Q_INDEX = 4