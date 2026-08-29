import sympy
from sympy import Symbol, Poly
from sympy.ntheory import factorint

x = Symbol('x')

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    Expected witness format: a tuple (q, f) where q is the order of the field
    and f is a SymPy expression for the polynomial in x.
    """
    try:
        if isinstance(witness, tuple):
            q, f = witness
        elif hasattr(witness, 'domain') and hasattr(witness.domain, 'order'):
            f = witness
            q = witness.domain.order
        else:
            q = witness.q
            f = witness.f
    except Exception:
        return [False, False, False, False]

    # H_1: F is a finite field of odd order q
    try:
        q = int(q)
        if q > 1 and q % 2 != 0:
            factors_q = factorint(q)
            h1 = len(factors_q) == 1
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: f(x) is a monic polynomial of degree n over F
    try:
        factors_q = factorint(q)
        p = list(factors_q.keys())[0]
        k = factors_q[p]
        if k == 1:
            from sympy.polys.domains import GF
            domain = GF(p)
        else:
            from sympy.polys.domains import FF
            domain = FF(p, k)
            
        f_poly_q = Poly(f, x, domain=domain)
        n = f_poly_q.degree()
        h2 = bool(f_poly_q.LC() == domain.one or f_poly_q.LC() == 1)
    except Exception:
        h2 = False

    # H_3: f(x) has distinct roots in its splitting field over F
    try:
        f_diff = f_poly_q.diff()
        g = f_poly_q.gcd(f_diff)
        h3 = bool(g.degree() == 0)
    except Exception:
        h3 = False

    # ¬Q: The discriminant of f(x) is a quadratic residue in F if and only if n ≡ r (mod 2) is FALSE
    try:
        # Calculate r: the number of irreducible factors of f(x) over F
        factors_list = f_poly_q.factor_list()
        r = sum(mult for fac, mult in factors_list[1])
        
        # Calculate the discriminant of f(x) over F
        res = f_poly_q.resultant(f_diff)
        sign_int = (-1)**(n*(n-1)//2)
        if sign_int == -1:
            disc_q = -res
        else:
            disc_q = res
            
        # Check if the discriminant is a quadratic residue in F using Euler's criterion
        power = (q - 1) // 2
        if k == 1:
            disc_val = int(disc_q) % p
            disc_pow = pow(disc_val, power, p)
            is_sq = (disc_pow == 1)
        else:
            disc_pow = disc_q ** power
            is_sq = bool(disc_pow == domain.one)
        
        # Check parity match
        parity_match = bool((n % 2) == (r % 2))
        
        # The conclusion is that is_sq == parity_match. We want the negation.
        neg_q = bool(is_sq != parity_match)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field of odd order q",
    "H_2: f(x) is a monic polynomial of degree n over F",
    "H_3: f(x) has distinct roots in its splitting field over F",
    "¬Q: The discriminant of f(x) is a quadratic residue in F if and only if n ≡ r (mod 2) is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3