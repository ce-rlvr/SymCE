import sympy
from sympy import Poly, Symbol, sympify
from sympy.ntheory import isprime

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            f, g = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        f = sympify(f)
        g = sympify(g)
        symbols = f.free_symbols | g.free_symbols
        symbols = {s for s in symbols if isinstance(s, Symbol)}
        if len(symbols) == 1:
            var = list(symbols)[0]
        elif len(symbols) == 0:
            var = Symbol('x')
        else:
            var = None
    except Exception:
        var = None

    # H1: R is a UFD (we verify the witness polynomials are in ZZ)
    h1_ok = False
    try:
        if var is not None:
            Poly(f, var, domain='ZZ')
            Poly(g, var, domain='ZZ')
            h1_ok = True
    except Exception:
        h1_ok = False

    # H2: g is an irreducible polynomial that divides f
    h2_ok = False
    try:
        if h1_ok:
            p_g = Poly(g, var, domain='ZZ')
            p_f = Poly(f, var, domain='ZZ')
            
            if p_g.is_zero:
                h2_ok = False
            else:
                # Check if g divides f
                q, r = p_f.div(p_g)
                divides = r.is_zero
                
                # Check if g is irreducible in ZZ[x]
                c = p_g.content()
                h = p_g.primitive()[1]
                if h.degree() == 0:
                    irreducible = isprime(abs(int(c)))
                else:
                    if abs(int(c)) != 1:
                        irreducible = False
                    else:
                        c_h, factors = h.factor_list()
                        irreducible = (len(factors) == 1 and factors[0][1] == 1)
                
                h2_ok = bool(divides and irreducible)
    except Exception:
        h2_ok = False

    # neg_Q: g is NOT primitive
    neg_q_ok = False
    try:
        if h1_ok:
            p_g = Poly(g, var, domain='ZZ')
            if p_g.is_zero:
                neg_q_ok = False
            else:
                c = p_g.content()
                # A polynomial in ZZ[x] is primitive iff the gcd of its coefficients is 1
                neg_q_ok = abs(int(c)) != 1
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: g is an irreducible polynomial that divides f",
    "¬Q: g is not primitive"
]

N_HYP = 2
NEG_Q_INDEX = 2