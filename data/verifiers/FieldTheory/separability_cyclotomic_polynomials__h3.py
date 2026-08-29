import sympy
from sympy import cyclotomic_poly, Symbol, gcd, Poly, isprime

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (n, K) where n is an integer and K is a field
    (represented by its characteristic p, or a SymPy domain object like QQ or GF(p)).
    """
    try:
        if len(witness) != 2:
            return [False, False, False]
        n, K_obj = witness
    except Exception:
        return [False, False, False]
        
    # H1: n is a positive integer
    try:
        n_val = int(n)
        h1 = (n_val == n) and (n_val > 0)
    except Exception:
        h1 = False
        
    # H2: K is a field such that the characteristic of K does not divide n
    try:
        try:
            # Try to interpret K_obj directly as the characteristic (int)
            p = int(K_obj)
        except Exception:
            # Otherwise, try to extract the characteristic from a domain object
            if hasattr(K_obj, 'characteristic'):
                char_val = K_obj.characteristic
                if callable(char_val):
                    p = int(char_val())
                else:
                    p = int(char_val)
            else:
                p = -1
                
        is_field = isinstance(p, int) and (p == 0 or isprime(p))
        if is_field:
            h2 = (p == 0) or (n_val % p != 0)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: Phi_n(x) is NOT separable over K (meaning it has repeated roots)
    try:
        phi = cyclotomic_poly(n_val, x)
        if p == 0:
            # Over characteristic 0, check gcd(phi, phi')
            d = Poly(gcd(phi, phi.diff(x)), x)
            neg_q = (d.degree() > 0)
        elif is_field:
            # Over characteristic p, check gcd(phi, phi') in GF(p)[x]
            phi_p = Poly(phi, x, domain=f'GF({p})')
            deriv = phi_p.diff(x)
            if deriv.is_zero:
                neg_q = True
            else:
                d = phi_p.gcd(deriv)
                neg_q = (d.degree() > 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: K is a field such that the characteristic of K does not divide n",
    "¬Q: The polynomial Phi_n(x) is not separable over K"
]

N_HYP = 2
NEG_Q_INDEX = 2