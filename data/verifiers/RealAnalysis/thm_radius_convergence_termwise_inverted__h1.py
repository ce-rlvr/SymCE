import sympy
from sympy import oo, limit, Abs

# Top-level setup for the witness namespace
n = sympy.Symbol('n', integer=True, positive=True)
x = sympy.Symbol('x', real=True)

def conditions(witness):
    # Extract a_n and R_given from witness
    try:
        if isinstance(witness, tuple):
            a_n, R_given = witness
        else:
            a_n = witness
            R_given = None
        a_n = sympy.sympify(a_n)
    except Exception:
        a_n = witness
        R_given = None

    # Find the symbol n in a_n and substitute with our positive integer n
    try:
        if hasattr(a_n, 'free_symbols'):
            free_symbols = a_n.free_symbols
            user_n = None
            if len(free_symbols) == 1:
                user_n = list(free_symbols)[0]
            elif len(free_symbols) > 1:
                n_sym = [s for s in free_symbols if s.name == 'n']
                if n_sym:
                    user_n = n_sym[0]
                else:
                    user_n = list(free_symbols)[0]
            
            if user_n is not None and user_n != n:
                a_n = a_n.subs(user_n, n)
    except Exception:
        pass

    # H_1: a_n != 0 for all n >= 0
    h1 = True
    try:
        for i in range(100):
            val = a_n.subs(n, i)
            if val == 0 or val.is_zero:
                h1 = False
                break
    except Exception:
        h1 = False

    # H_2: lim_{n -> oo} |a_n|^(1/n) exists
    h2 = False
    L = None
    try:
        L = limit(Abs(a_n)**(1/n), n, oo)
        # In sympy, if the limit does not exist, it might return AccumBounds or an unevaluated Limit
        if not L.has(sympy.AccumBounds) and not isinstance(L, sympy.Limit):
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: The power series sum_{n=0}^oo 1/a_n x^n does NOT have a radius of convergence equal to 1/R
    neg_q = False
    try:
        if h2 and L is not None:
            # Compute R_prime (radius of convergence of the inverted series)
            L_prime = limit(Abs(1/a_n)**(1/n), n, oo)
            if L_prime == oo:
                R_prime = 0
            elif L_prime == 0:
                R_prime = oo
            else:
                R_prime = 1/L_prime

            # Determine R (radius of convergence of the original series)
            if R_given is not None:
                R = R_given
            else:
                if L == oo:
                    R = 0
                elif L == 0:
                    R = oo
                else:
                    R = 1/L

            # Check if R_prime == 1/R
            if R == 0:
                # 1/0 is undefined in standard real analysis, so it cannot be equal to R_prime
                neg_q = True
            else:
                if R == oo:
                    inv_R = 0
                else:
                    inv_R = 1/R
                neg_q = not bool(sympy.Eq(R_prime, inv_R))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a_n != 0 for all n >= 0",
    "H_2: The limit lim_{n -> oo} |a_n|^(1/n) exists",
    "¬Q: The power series sum_{n=0}^oo 1/a_n x^n does NOT have a radius of convergence equal to 1/R"
]

N_HYP = 2
NEG_Q_INDEX = 2