import sympy as sp

# Top-level setup
x = sp.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The missing hypothesis is lambda > 0.
    Witness is expected to be a tuple: (f, d, lambda) or (f, lambda) assuming d=1.
    """
    try:
        if len(witness) == 3:
            f, d, lam = witness
        elif len(witness) == 2:
            f, lam = witness
            d = 1
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: f is a Lebesgue integrable function in L^1(R^d)
    try:
        # We integrate over R^1 as a representative check
        integral = sp.integrate(sp.Abs(f), (x, -sp.oo, sp.oo)).doit()
        try:
            h1_ok = bool(integral < sp.oo)
        except TypeError:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: Mf(x) is the centered Hardy-Littlewood maximal function
    # This is a definitional hypothesis, so it holds by definition for the context.
    h2_ok = True

    # neg_Q: The conclusion FAILS at the witness
    # Conclusion: m({x : Mf(x) > lambda}) <= (3^d / lambda) * ||f||_1
    try:
        try:
            is_neg = bool(lam < 0)
        except TypeError:
            is_neg = False
            
        try:
            is_zero = bool(lam == 0)
        except TypeError:
            is_zero = False

        if is_neg:
            # If lambda < 0, Mf(x) >= 0 > lambda for all x, so the measure is infinity.
            lhs = sp.oo
            rhs = (3**d / lam) * integral
            try:
                is_le = bool(lhs <= rhs)
            except TypeError:
                is_le = False
            neg_q_ok = not is_le
        elif is_zero:
            # If lambda == 0, the RHS is division by zero, making the inequality invalid/fail.
            neg_q_ok = True
        else:
            # If lambda > 0, the theorem is true, so the conclusion holds (does not fail).
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a Lebesgue integrable function in L^1(R^d)",
    "H_2: Mf(x) is the centered Hardy-Littlewood maximal function",
    "¬Q: The weak type (1,1) inequality fails"
]

N_HYP = 2
NEG_Q_INDEX = 2