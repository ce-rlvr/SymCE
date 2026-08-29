import sympy
from sympy import Symbol, Interval, diff, factorial, solveset, Eq, EmptySet, S
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f and its first n derivatives are continuous on the closed interval from a to b",
    "¬Q: There does not exist c in the open interval from a to b satisfying the Cauchy remainder equation"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness tuple (f, a, b, n), checks if it is a valid counterexample.
    f is a sympy expression in terms of x.
    a, b are real numbers (a < b).
    n is a non-negative integer.
    """
    try:
        f, a, b, n = witness
    except Exception:
        return [False, False]
        
    # H_1: f and its first n derivatives are continuous on the closed interval from a to b
    h1_ok = False
    try:
        if a < b and n >= 0 and int(n) == n:
            n = int(n)
            domain = Interval(a, b)
            is_continuous = True
            for k in range(n + 1):
                deriv = diff(f, x, k)
                cd = continuous_domain(deriv, x, domain)
                if not domain.is_subset(cd):
                    is_continuous = False
                    break
            h1_ok = is_continuous
    except Exception:
        h1_ok = False

    # neg_Q: There does NOT exist c in (a, b) such that
    # f(b) = sum_{k=0}^n f^{(k)}(a)/k! (b-a)^k + f^{(n+1)}(c)/n! (b-c)^n (b-a)
    neg_q_ok = False
    try:
        poly_sum = S.Zero
        for k in range(n + 1):
            term = diff(f, x, k).subs(x, a) / factorial(k) * (b - a)**k
            poly_sum += term
        
        R = f.subs(x, b) - poly_sum
        
        c = Symbol('c', real=True)
        deriv_np1 = diff(f, x, n + 1).subs(x, c)
        rhs = deriv_np1 / factorial(n) * (b - c)**n * (b - a)
        
        eq = Eq(rhs, R)
        sol = solveset(eq, c, domain=Interval.open(a, b))
        
        if sol is EmptySet:
            neg_q_ok = True
        elif sol.is_FiniteSet:
            any_valid = False
            for pt in sol:
                try:
                    # Verify that the (n+1)-th derivative actually exists at pt
                    # by checking if the left and right limits of the n-th derivative are equal
                    deriv_n = diff(f, x, n)
                    ld = deriv_n.diff(x).limit(x, pt, dir='-')
                    rd = deriv_n.diff(x).limit(x, pt, dir='+')
                    
                    if ld == rd and ld not in (S.Infinity, S.NegativeInfinity, S.ComplexInfinity, S.NaN) and not ld.has(sympy.I):
                        val = (ld / factorial(n)) * (b - pt)**n * (b - a)
                        diff_val = sympy.simplify(val - R)
                        if diff_val == 0:
                            any_valid = True
                            break
                        try:
                            if abs(float(diff_val)) < 1e-9:
                                any_valid = True
                                break
                        except Exception:
                            pass
                except Exception:
                    # If we cannot definitively rule it out, assume it might be valid to be safe
                    any_valid = True
            
            if not any_valid:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]