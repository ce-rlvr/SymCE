import sympy
from sympy import factor_list, diff, isprime, Poly
from sympy.abc import x, t

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (char_F, p, f, w_x, w_t) or (char_F, p, f)
    where:
      - char_F is the characteristic of the base field F = F_{char_F}(w_t)
      - p is the prime mentioned in the hypothesis
      - f is the minimal polynomial of the extension E = F[w_x]/(f)
      - w_x, w_t are the sympy symbols used in f (defaults to sympy.abc.x, sympy.abc.t)
    """
    try:
        if len(witness) == 5:
            char_F, p, f, w_x, w_t = witness
        elif len(witness) == 3:
            char_F, p, f = witness
            w_x, w_t = x, t
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: E/F is a finite field extension
    try:
        h1 = False
        if isprime(char_F) and isprime(p):
            f_poly = Poly(f, w_x, w_t, modulus=char_F)
            deg_x = f_poly.degree(w_x)
            if deg_x >= 1:
                coeff, factors = factor_list(f, modulus=char_F)
                if len(factors) == 1 and factors[0][1] == 1:
                    h1 = True
    except Exception:
        h1 = False

    # H_2: The degree of E over F is not divisible by p
    try:
        h2 = False
        if h1:
            f_poly = Poly(f, w_x, w_t, modulus=char_F)
            deg_x = f_poly.degree(w_x)
            h2 = (deg_x % p != 0)
    except Exception:
        h2 = False

    # ¬Q: The field extension E/F is NOT separable
    try:
        neg_q = False
        df = diff(f, w_x)
        df_poly = Poly(df, w_x, w_t, modulus=char_F)
        neg_q = df_poly.is_zero
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E over F is a finite field extension",
    "H_2: The degree of E over F is not divisible by p",
    "¬Q: The field extension E over F is not separable"
]

N_HYP = 2
NEG_Q_INDEX = 2