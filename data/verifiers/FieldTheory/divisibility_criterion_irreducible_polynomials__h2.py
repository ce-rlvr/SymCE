import sympy
from sympy import Symbol, Poly, sympify
from sympy.polys.domains import GF
from sympy.ntheory import factorint

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            q, n, f, d = witness
        elif len(witness) == 3:
            q, n, f = witness
            f = sympify(f)
            d = Poly(f, x).degree()
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: F_q is a finite field (q is a prime power)
    try:
        q_val = int(q)
        if q_val < 2:
            h1 = False
        else:
            factors = factorint(q_val)
            h1 = len(factors) == 1
    except Exception:
        h1 = False

    # H2: n is a positive integer
    try:
        n_val = int(n)
        h2 = n_val > 0
    except Exception:
        h2 = False

    # neg_Q: f(x) divides x^{q^n} - x in F_q[x] iff d divides n
    try:
        f_expr = sympify(f)
        q_val = int(q)
        n_val = int(n)
        d_val = int(d)
        
        # We evaluate over GF(q_val). Note that sympy's GF requires q_val to be prime.
        # If the witness uses a prime power that is not prime, this will raise an exception
        # and safely return False. The witness can simply provide a prime q.
        f_poly = Poly(f_expr, x, domain=GF(q_val))
        
        if f_poly.is_zero:
            divides = False
        elif f_poly.degree() <= 0:
            divides = True
        else:
            res = Poly(1, x, domain=GF(q_val))
            base = Poly(x, x, domain=GF(q_val))
            exp = q_val**n_val
            
            # Modular exponentiation: x^(q^n) mod f(x)
            while exp > 0:
                if exp % 2 == 1:
                    res = (res * base) % f_poly
                base = (base * base) % f_poly
                exp //= 2
                
            expected = Poly(x, x, domain=GF(q_val)) % f_poly
            divides = (res == expected)
            
        d_divides_n = (d_val != 0) and (n_val % d_val == 0)
        
        neg_q = (divides != d_divides_n)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: F_q is a finite field",
    "H_2: n is a positive integer",
    "¬Q: f(x) divides x^(q^n) - x in F_q polynomials iff d divides n fails"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2