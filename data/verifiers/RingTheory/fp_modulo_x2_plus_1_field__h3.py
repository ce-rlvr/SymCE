import sympy
from sympy import Symbol, Poly, isprime, sympify

x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (p, I) or a dictionary {'p': p, 'I': I},
    where p is an integer and I is a polynomial expression.
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            I = witness.get('I', x**2 + 1)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                p, I = witness
            else:
                p = witness[0]
                I = x**2 + 1
        else:
            p = witness
            I = x**2 + 1
    except Exception:
        return [False, False, False]

    # H_1: Let p be an odd prime number.
    try:
        p = int(p)
        h1 = isprime(p) and p % 2 == 1
    except Exception:
        h1 = False

    # H_2: Let F_p[x] be the polynomial ring over the finite field with p elements.
    # We verify this by checking if I is a valid polynomial in F_p[x].
    try:
        if not h1:
            h2 = False
        else:
            if isinstance(I, str):
                I = I.replace('^', '**')
            I_expr = sympify(I)
            free_syms = I_expr.free_symbols
            if len(free_syms) == 1:
                gen = list(free_syms)[0]
            else:
                gen = x
            poly_I = Poly(I_expr, gen, domain=f'GF({p})')
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: The factor ring F_p[x]/I is a field if and only if p = 3 mod 4.
    # We want this conclusion to FAIL, so we check if the equivalence is broken.
    try:
        if not h2:
            neg_q = False
        else:
            deg = poly_I.degree()
            try:
                deg_ok = int(deg) >= 1
            except Exception:
                deg_ok = False
            
            # F_p[x]/I is a field iff I is irreducible and has degree >= 1
            is_field = deg_ok and bool(poly_I.is_irreducible)
            p_mod_4_is_3 = (p % 4 == 3)
            
            # The conclusion fails if the truth values of is_field and p_mod_4_is_3 differ
            neg_q = bool(is_field != p_mod_4_is_3)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: F_p(x) is the polynomial ring over the finite field with p elements",
    "neg_Q: The condition that F_p(x)/I is a field is NOT equivalent to p == 3 mod 4"
]

N_HYP = 2
NEG_Q_INDEX = 2