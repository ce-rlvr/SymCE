import sympy

# Top-level setup
n = sympy.Symbol('n', integer=True, nonnegative=True)
x = sympy.Symbol('x')

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: The power series is defined as sum B_n x^n",
    "¬Q: The radius of convergence is not exactly 0"
]

def conditions(witness):
    try:
        # Extract the general term B_n from the witness
        if callable(witness):
            B_n = witness(n)
        elif isinstance(witness, sympy.Sum):
            term = witness.function
            # Assuming the sum is of the form Sum(B_n * x**n, (n, 0, oo))
            B_n = term.subs(x, 1)
        else:
            B_n = sympy.sympify(witness)
            
        # H_1: Check if B_n is a valid sequence of numbers
        h1 = True
        for i in range(10):
            val = B_n.subs(n, i)
            if not (val.is_number and val.is_finite):
                h1 = False
                break
    except Exception:
        h1 = False

    try:
        if callable(witness):
            B_n = witness(n)
        elif isinstance(witness, sympy.Sum):
            term = witness.function
            B_n = term.subs(x, 1)
        else:
            B_n = sympy.sympify(witness)

        # Calculate the limit of |B_n|^(1/n) as n -> oo to find 1/R
        L = sympy.limit(sympy.Abs(B_n)**(1/n), n, sympy.oo)
        
        if isinstance(L, sympy.Limit):
            # Fallback to the ratio test if the root test limit is unevaluated
            ratio = sympy.Abs(B_n / B_n.subs(n, n + 1))
            L_ratio = sympy.limit(ratio, n, sympy.oo)
            if L_ratio == 0:
                neg_q = False
            elif L_ratio != 0 and not isinstance(L_ratio, sympy.Limit):
                neg_q = True
            else:
                neg_q = False
        else:
            # If L == oo, then R = 0. We want neg_q to be True when R != 0.
            neg_q = (L != sympy.oo)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]