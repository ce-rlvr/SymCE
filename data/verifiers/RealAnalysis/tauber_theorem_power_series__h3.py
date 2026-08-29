import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
n = sp.Symbol('n', integer=True, nonnegative=True)
x = sp.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: Power series converges to a function f(x) for all x in (-1, 1)",
    "H_2: Limit of f(x) as x -> 1- exists and is finite",
    "¬Q: The series sum(a_n) diverges or its sum is not equal to L"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Check if witness is a valid expression in n
    if not isinstance(witness, sp.Expr):
        try:
            witness = sp.sympify(witness)
        except Exception:
            return [False, False, False]
            
    if not witness.free_symbols.issubset({n}):
        return [False, False, False]

    # H_1: Power series converges to a function f(x) for all x in (-1, 1)
    h1_ok = False
    f_x_expr = None
    try:
        # Evaluate the sum
        f_x = sp.summation(witness * x**n, (n, 0, sp.oo))
        f_x_expr = f_x
        
        # If the result is a Piecewise, extract the expression valid for x in (-1, 1)
        if isinstance(f_x, sp.Piecewise):
            for expr, cond in f_x.args:
                try:
                    if cond == True:
                        f_x_expr = expr
                        break
                    # Check if the condition holds for values close to 1 and -1
                    c1 = cond.subs(x, sp.Rational(999, 1000))
                    c2 = cond.subs(x, sp.Rational(-999, 1000))
                    if c1 == True and c2 == True:
                        f_x_expr = expr
                        break
                except Exception:
                    pass
        
        # If sympy couldn't evaluate the sum, it will contain a Sum object
        if f_x_expr.has(sp.Sum):
            h1_ok = False
        else:
            # Check if the function is well-defined and finite at x = 1/2
            val = f_x_expr.subs(x, sp.Rational(1, 2))
            if val.is_finite == True:
                h1_ok = True
            else:
                h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: Limit of f(x) as x -> 1- exists and is finite
    h2_ok = False
    L = sp.nan
    try:
        if f_x_expr is not None and not f_x_expr.has(sp.Sum):
            L = sp.limit(f_x_expr, x, 1, dir='-')
            if L.is_finite == True:
                h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The series sum(a_n) diverges or its sum is not equal to L
    neg_q = False
    try:
        sum_an = sp.Sum(witness, (n, 0, sp.oo))
        is_conv = sum_an.is_convergent()
        
        if is_conv is False:
            neg_q = True
        elif is_conv is True:
            sum_val = sum_an.doit()
            if sum_val.is_finite == False:
                neg_q = True
            else:
                diff = sp.simplify(sum_val - L)
                if diff == 0:
                    neg_q = False
                else:
                    neg_q = True
        else:
            # If sympy cannot definitively determine convergence
            sum_val = sum_an.doit()
            if sum_val.has(sp.Sum):
                # If it remains unevaluated, check if terms go to 0
                term_limit = sp.limit(witness, n, sp.oo)
                if term_limit != 0:
                    neg_q = True
                else:
                    # Fallback for verifier: assume it doesn't converge to L
                    neg_q = True
            else:
                if sum_val.is_finite == False:
                    neg_q = True
                else:
                    diff = sp.simplify(sum_val - L)
                    if diff == 0:
                        neg_q = False
                    else:
                        neg_q = True
    except Exception:
        neg_q = True

    return [h1_ok, h2_ok, neg_q]