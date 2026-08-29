import math
from functools import reduce
from sympy import symbols, sympify, sqf_list

# Top-level setup for witness expressions
x, y = symbols('x y')

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (n, g) or (K, n, g).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                n, g = witness
            elif len(witness) == 3:
                _, n, g = witness
            else:
                return [False] * 4
        else:
            return [False] * 4
    except Exception:
        return [False] * 4

    try:
        g = sympify(g)
        n = int(sympify(n))
    except Exception:
        return [False] * 4

    try:
        # Ensure g is an expression in x only
        if len(g.free_symbols - {x}) > 0:
            return [False] * 4
    except Exception:
        pass

    # H_1: K is an algebraically closed field
    h1_ok = True

    # H_2: n >= 2 is an integer
    try:
        h2_ok = n >= 2
    except Exception:
        h2_ok = False

    # H_3: There exists a root alpha in K of g(x) such that the multiplicity of alpha 
    # as a root of g(x) is coprime to n.
    try:
        if g == 0:
            h3_ok = False
        else:
            g_simp = g.cancel()
            num, den = g_simp.as_numer_denom()
            
            sqf = sqf_list(num)
            h3_ok = False
            for f, m in sqf[1]:
                if x in f.free_symbols:
                    if math.gcd(int(m), n) == 1:
                        h3_ok = True
                        break
    except Exception:
        h3_ok = False

    # ¬Q: The polynomial y^n - g(x) is reducible
    try:
        if g == 0:
            neg_q_ok = (n >= 2)
        else:
            num, den = g.cancel().as_numer_denom()
            if x in den.free_symbols:
                # g(x) is a rational function, so y^n - g(x) is not a polynomial
                neg_q_ok = True
            else:
                # Over an algebraically closed field, y^n - g(x) is reducible iff g(x) is a p-th power 
                # for some prime p dividing n. This is equivalent to the GCD of all root multiplicities 
                # sharing a common factor with n.
                sqf = sqf_list(num)
                mults = [int(m) for f, m in sqf[1] if x in f.free_symbols]
                if not mults:
                    # If g(x) is a constant, y^n - c is reducible over C for any n >= 2
                    neg_q_ok = (n >= 2)
                else:
                    g_mult_gcd = reduce(math.gcd, mults)
                    neg_q_ok = math.gcd(g_mult_gcd, n) > 1
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: n >= 2 is an integer",
    "H_3: There exists a root alpha in K of g(x) such that the multiplicity of alpha as a root of g(x) is coprime to n",
    "¬Q: The polynomial y^n - g(x) is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3