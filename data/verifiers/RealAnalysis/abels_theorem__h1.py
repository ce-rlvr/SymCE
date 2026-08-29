import sympy as sp

n = sp.Symbol('n', integer=True, nonnegative=True)
x = sp.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (a_n, R) where a_n is a sympy expression 
    in terms of n (or a callable returning one), and R is a real number.
    """
    try:
        a_n, R = witness
    except Exception:
        return [False, False, False]
        
    try:
        if callable(a_n):
            a_expr = a_n(n)
        else:
            a_expr = a_n
        a_expr = sp.sympify(a_expr)
    except Exception:
        return [False, False, False]

    # Find the first valid index to start the sum (usually 0, but allows leniency if undefined at 0)
    start_n = 0
    for i in range(10):
        try:
            val = a_expr.subs(n, i)
            if val.is_number and val.is_finite:
                start_n = i
                break
        except Exception:
            pass

    # H_1: Suppose the series \sum_{n=0}^{\infty} a_n R^n converges.
    h1_ok = False
    try:
        if R == 0:
            a_0 = a_expr.subs(n, 0)
            if a_0.is_number and a_0.is_finite:
                h1_ok = True
        else:
            term = a_expr * (R**n)
            s = sp.Sum(term, (n, start_n, sp.oo))
            try:
                conv = s.is_convergent()
            except Exception:
                conv = None
                
            if conv is not None:
                h1_ok = bool(conv)
            else:
                val = s.doit()
                if val.is_number and val.is_finite:
                    h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: Let f(x) = \sum_{n=0}^{\infty} a_n x^n for x \in (-R, R).
    # This is a definition, so it holds as long as the witness is well-formed.
    h2_ok = True if a_expr is not None else False

    # ¬Q: The limit \lim_{x \to R^-} f(x) does not exist or does not equal the sum.
    # The conclusion fails exactly when the series diverges for x < R (i.e., x approaches R from the left).
    # This happens if and only if R <= 0 and the radius of convergence rho is exactly |R|.
    neg_q = False
    try:
        try:
            r_le_0 = bool(R <= 0)
        except TypeError:
            r_le_0 = False

        rho = None
        # Attempt Ratio Test
        try:
            ratio = sp.Abs(a_expr / a_expr.subs(n, n+1))
            ratio = sp.combsimp(ratio)
            rho_val = sp.limit(ratio, n, sp.oo)
            if rho_val.is_number or rho_val == sp.oo:
                rho = rho_val
        except Exception:
            pass
        
        # Attempt Root Test if Ratio Test fails
        if rho is None:
            try:
                root = sp.Abs(a_expr)**(-1/n)
                rho_val = sp.limit(root, n, sp.oo)
                if rho_val.is_number or rho_val == sp.oo:
                    rho = rho_val
            except Exception:
                pass
        
        if rho is not None:
            if r_le_0:
                diff = sp.simplify(rho - sp.Abs(R))
                if diff == 0:
                    neg_q = True
                else:
                    try:
                        if abs(float(diff)) < 1e-9:
                            neg_q = True
                    except Exception:
                        pass
        else:
            # Fallback: Check if the series diverges at a point slightly less than R
            if r_le_0:
                test_term = a_expr * ((R - sp.Rational(1, 100))**n)
                test_s = sp.Sum(test_term, (n, start_n, sp.oo))
                try:
                    conv = test_s.is_convergent()
                except Exception:
                    conv = None
                if conv is sp.false:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: The series sum_{n=0}^{infty} a_n R^n converges",
    "H_2: f(x) is defined as sum_{n=0}^{infty} a_n x^n for x in (-R, R)",
    "¬Q: The limit lim_{x -> R^-} f(x) does not exist or does not equal the sum"
]

N_HYP = 2
NEG_Q_INDEX = 2