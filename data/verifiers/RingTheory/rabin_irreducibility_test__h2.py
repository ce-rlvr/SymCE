import sympy
from sympy import Poly
from sympy.abc import x
from sympy.ntheory import primefactors

# Top-level setup
# x is imported from sympy.abc and available for witness expressions

def is_prime_power(q):
    if type(q) is not int or q < 2:
        return False
    factors = primefactors(q)
    return len(factors) == 1

def poly_powmod(base, exp, mod_poly, q):
    res = Poly(1, x, domain=sympy.GF(q))
    base = base % mod_poly
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod_poly
        base = (base * base) % mod_poly
        exp //= 2
    return res

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
            f = witness.get('f')
        else:
            q, n, f = witness
    except Exception:
        return [False, False]

    # H1: F_q is a finite field of order q
    try:
        h1 = is_prime_power(q) and type(n) is int and n >= 1
        if h1:
            poly_f = Poly(f, x, domain=sympy.GF(q))
            if poly_f.degree() < 1:
                h1 = False
    except Exception:
        h1 = False

    # Conclusion: f(x) is irreducible over F_q iff f(x) divides x^{q^n} - x and gcd(f(x), x^{q^{n/r}} - x) = 1 for all prime divisors r of n.
    try:
        if not h1:
            neg_q = False
        else:
            poly_f = Poly(f, x, domain=sympy.GF(q))
            is_irred = poly_f.is_irreducible
            
            x_poly = Poly(x, x, domain=sympy.GF(q))
            
            # Check if f(x) divides x^{q^n} - x
            rem = poly_powmod(x_poly, q**n, poly_f, q)
            divides = (rem == x_poly % poly_f)
            
            # Check gcd condition
            gcds_one = True
            for r in primefactors(n):
                rem_r = poly_powmod(x_poly, q**(n//r), poly_f, q)
                gcd_poly = poly_f.gcd(rem_r - x_poly)
                if gcd_poly.degree() > 0:
                    gcds_one = False
                    break
                    
            q_holds = divides and gcds_one
            
            # The conclusion is P iff Q
            conclusion = (is_irred == q_holds)
            neg_q = not conclusion
            
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field of order q",
    "¬Q: The equivalence 'f(x) is irreducible iff f(x) divides x^{q^n} - x and gcd(f(x), x^{q^{n/r}} - x) = 1 for all prime divisors r of n' fails"
]

N_HYP = 1
NEG_Q_INDEX = 1